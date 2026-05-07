"""
Target-Constrained Filter (TCF) for HSDNet.

This module implements the post-processing TCF described in the HSDNet paper:
defect predictions are retained only when they have valid spatial association
with their corresponding host-object predictions.

Default class setting for the self-built transmission line dataset:
    0: insulator  -> host object
    1: broken     -> constrained defect
    2: flashover  -> constrained defect
    3: hammer     -> normal component, not filtered by default
    4: corrode    -> constrained defect
    5: nest       -> independent target, not filtered by default

Recommended placement:
    utils/tcf.py or tcf.py

Typical usage with Ultralytics YOLO:
    from ultralytics import YOLO
    from tcf import TargetConstrainedFilter

    model = YOLO("runs/train/hsdnet/weights/best.pt")
    results = model.predict(source="dataset/images/test", conf=0.25, iou=0.7, save=False)

    tcf = TargetConstrainedFilter(tau=0.3)
    filtered_results = tcf.filter_results(results)

    for r in filtered_results:
        r.save(filename="runs/detect/tcf/" + r.path.split("/")[-1])
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple, Union

import torch

try:
    import cv2  # type: ignore
except Exception:
    cv2 = None


TensorLike = Union[torch.Tensor, Sequence[Sequence[float]]]


@dataclass(frozen=True)
class TCFStats:
    """Statistics for one TCF filtering operation."""

    total: int
    hosts: int
    defects: int
    removed_defects: int
    kept: int


class TargetConstrainedFilter:
    """
    Target-Constrained Filter based on host-defect spatial dependency.

    The module is designed as an inference-stage post-processing component.
    It does not change the detection network, loss function, or training process.

    Args:
        tau: IoU threshold for validating host-defect spatial association.
        host_class_ids: Class IDs regarded as host objects.
        defect_class_ids: Class IDs regarded as constrained defect objects.
        host_class_names: Optional host class names. Used when model class names
            are available from Ultralytics results.
        defect_class_names: Optional defect class names. Used when model class
            names are available from Ultralytics results.
        filter_when_no_host: If True, constrained defects are removed when no
            host prediction exists in the same image.
        class_col: Class-index column in a detection tensor. Ultralytics Boxes
            usually use [x1, y1, x2, y2, conf, cls], so class_col=5.
    """

    def __init__(
        self,
        tau: float = 0.3,
        host_class_ids: Sequence[int] = (0,),
        defect_class_ids: Sequence[int] = (1, 2, 4),
        host_class_names: Sequence[str] = ("insulator",),
        defect_class_names: Sequence[str] = ("broken", "flashover", "corrode"),
        filter_when_no_host: bool = True,
        class_col: int = 5,
    ) -> None:
        if tau < 0:
            raise ValueError("tau must be non-negative.")

        self.tau = float(tau)
        self.host_class_ids = tuple(int(i) for i in host_class_ids)
        self.defect_class_ids = tuple(int(i) for i in defect_class_ids)
        self.host_class_names = tuple(self._norm_name(n) for n in host_class_names)
        self.defect_class_names = tuple(self._norm_name(n) for n in defect_class_names)
        self.filter_when_no_host = bool(filter_when_no_host)
        self.class_col = int(class_col)

    @staticmethod
    def _norm_name(name: str) -> str:
        return str(name).strip().lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def box_iou(boxes1: torch.Tensor, boxes2: torch.Tensor) -> torch.Tensor:
        """
        Calculate IoU between two box sets in xyxy format.

        Args:
            boxes1: Tensor with shape [N, 4], format [x1, y1, x2, y2].
            boxes2: Tensor with shape [M, 4], format [x1, y1, x2, y2].

        Returns:
            IoU tensor with shape [N, M].
        """
        if boxes1.numel() == 0 or boxes2.numel() == 0:
            return boxes1.new_zeros((boxes1.shape[0], boxes2.shape[0]))

        boxes1 = boxes1.float()
        boxes2 = boxes2.float()

        area1 = (boxes1[:, 2] - boxes1[:, 0]).clamp(min=0) * (
            boxes1[:, 3] - boxes1[:, 1]
        ).clamp(min=0)
        area2 = (boxes2[:, 2] - boxes2[:, 0]).clamp(min=0) * (
            boxes2[:, 3] - boxes2[:, 1]
        ).clamp(min=0)

        lt = torch.maximum(boxes1[:, None, :2], boxes2[:, :2])
        rb = torch.minimum(boxes1[:, None, 2:4], boxes2[:, 2:4])
        wh = (rb - lt).clamp(min=0)
        inter = wh[:, :, 0] * wh[:, :, 1]
        union = area1[:, None] + area2 - inter

        return inter / union.clamp(min=1e-6)

    def _ids_from_names(
        self,
        names: Optional[Union[Dict[int, str], Sequence[str]]],
        target_names: Sequence[str],
        fallback_ids: Sequence[int],
    ) -> Tuple[int, ...]:
        """Resolve class IDs from class names; fall back to predefined IDs."""
        if names is None:
            return tuple(fallback_ids)

        if isinstance(names, dict):
            items = names.items()
        else:
            items = enumerate(names)

        target_set = {self._norm_name(n) for n in target_names}
        matched = [int(i) for i, name in items if self._norm_name(name) in target_set]

        return tuple(matched) if matched else tuple(fallback_ids)

    def resolve_class_ids(
        self,
        names: Optional[Union[Dict[int, str], Sequence[str]]] = None,
    ) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """
        Resolve host and defect class IDs.

        Args:
            names: Optional class-name mapping from a YOLO model or result.

        Returns:
            A tuple: (host_ids, defect_ids).
        """
        host_ids = self._ids_from_names(
            names,
            self.host_class_names,
            self.host_class_ids,
        )
        defect_ids = self._ids_from_names(
            names,
            self.defect_class_names,
            self.defect_class_ids,
        )
        return host_ids, defect_ids

    def filter_detections(
        self,
        detections: TensorLike,
        names: Optional[Union[Dict[int, str], Sequence[str]]] = None,
        return_stats: bool = False,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, TCFStats]]:
        """
        Filter a detection tensor using TCF.

        Args:
            detections: Tensor-like object with shape [N, >=6]. The first four
                columns must be xyxy boxes. The class column is class_col.
            names: Optional class-name mapping. If provided, host/defect class
                IDs are resolved by class names.
            return_stats: If True, also return filtering statistics.

        Returns:
            Filtered detection tensor, or (filtered tensor, TCFStats).
        """
        det = torch.as_tensor(detections)

        if det.ndim != 2:
            raise ValueError("detections must be a 2D tensor with shape [N, >=6].")

        if det.shape[1] <= max(3, self.class_col):
            raise ValueError(
                f"detections must contain xyxy boxes and class column {self.class_col}."
            )

        if det.shape[0] == 0:
            stats = TCFStats(total=0, hosts=0, defects=0, removed_defects=0, kept=0)
            return (det, stats) if return_stats else det

        host_ids, defect_ids = self.resolve_class_ids(names)

        device = det.device
        cls = det[:, self.class_col].long()

        host_ids_t = torch.tensor(host_ids, device=device, dtype=torch.long)
        defect_ids_t = torch.tensor(defect_ids, device=device, dtype=torch.long)

        if len(host_ids) > 0:
            host_mask = torch.isin(cls, host_ids_t)
        else:
            host_mask = torch.zeros_like(cls, dtype=torch.bool)

        if len(defect_ids) > 0:
            defect_mask = torch.isin(cls, defect_ids_t)
        else:
            defect_mask = torch.zeros_like(cls, dtype=torch.bool)

        keep_mask = torch.ones(det.shape[0], device=device, dtype=torch.bool)

        host_count = int(host_mask.sum().item())
        defect_count = int(defect_mask.sum().item())
        removed = 0

        if defect_count > 0:
            defect_indices = torch.nonzero(defect_mask, as_tuple=False).flatten()

            if host_count == 0:
                if self.filter_when_no_host:
                    keep_mask[defect_indices] = False
                    removed = defect_count
            else:
                defect_boxes = det[defect_mask, :4]
                host_boxes = det[host_mask, :4]

                ious = self.box_iou(defect_boxes, host_boxes)
                max_iou = (
                    ious.max(dim=1).values
                    if ious.numel()
                    else ious.new_zeros((defect_count,))
                )

                valid_defects = max_iou >= self.tau
                keep_mask[defect_indices] = valid_defects
                removed = int((~valid_defects).sum().item())

        filtered = det[keep_mask]

        stats = TCFStats(
            total=int(det.shape[0]),
            hosts=host_count,
            defects=defect_count,
            removed_defects=removed,
            kept=int(filtered.shape[0]),
        )

        return (filtered, stats) if return_stats else filtered

    def filter_result(self, result, return_stats: bool = False):
        """
        Apply TCF to one Ultralytics Results object.

        The original result object is not modified. A shallow copy with updated
        boxes is returned.
        """
        if not hasattr(result, "boxes") or result.boxes is None:
            stats = TCFStats(total=0, hosts=0, defects=0, removed_defects=0, kept=0)
            return (result, stats) if return_stats else result

        boxes = result.boxes
        data = boxes.data
        names = getattr(result, "names", None)

        filtered_data, stats = self.filter_detections(
            data,
            names=names,
            return_stats=True,
        )

        out = copy.copy(result)

        if hasattr(out, "update"):
            out.update(boxes=filtered_data)
        else:
            try:
                from ultralytics.engine.results import Boxes

                out.boxes = Boxes(filtered_data, result.orig_shape)
            except Exception as exc:
                raise RuntimeError(
                    "Unable to update Ultralytics result boxes. Please upgrade ultralytics "
                    "or use filter_detections() directly on result.boxes.data."
                ) from exc

        return (out, stats) if return_stats else out

    def filter_results(self, results, return_stats: bool = False):
        """
        Apply TCF to a list of Ultralytics Results objects.

        Args:
            results: A Results object or a list/tuple of Results objects.
            return_stats: If True, return both filtered results and statistics.
        """
        if isinstance(results, (list, tuple)):
            filtered = []
            stats_list = []

            for r in results:
                fr, st = self.filter_result(r, return_stats=True)
                filtered.append(fr)
                stats_list.append(st)

            return (filtered, stats_list) if return_stats else filtered

        filtered_result, stats = self.filter_result(results, return_stats=True)

        return (filtered_result, stats) if return_stats else filtered_result

    __call__ = filter_results


def save_yolo_txt(result, filename: Union[str, Path]) -> None:
    """
    Save filtered detections in YOLO txt format.

    Output columns:
        cls x_center y_center width height confidence

    Coordinates are normalized by image width and height.
    """
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)

    if not hasattr(result, "boxes") or result.boxes is None or len(result.boxes) == 0:
        filename.write_text("", encoding="utf-8")
        return

    h, w = result.orig_shape[:2]
    boxes = result.boxes

    xyxy = boxes.xyxy.detach().cpu()
    conf = boxes.conf.detach().cpu()
    cls = boxes.cls.detach().cpu().long()

    xywh = torch.empty_like(xyxy)
    xywh[:, 0] = (xyxy[:, 0] + xyxy[:, 2]) / 2 / w
    xywh[:, 1] = (xyxy[:, 1] + xyxy[:, 3]) / 2 / h
    xywh[:, 2] = (xyxy[:, 2] - xyxy[:, 0]) / w
    xywh[:, 3] = (xyxy[:, 3] - xyxy[:, 1]) / h

    lines = []

    for c, box, cf in zip(cls.tolist(), xywh.tolist(), conf.tolist()):
        lines.append(
            f"{c} {box[0]:.6f} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f} {cf:.6f}"
        )

    filename.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run YOLO inference with HSDNet TCF post-processing."
    )

    parser.add_argument(
        "--model",
        type=str,
        default="runs/train/hsdnet/weights/best.pt",
        help="Path to model weights.",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="dataset/images/test",
        help="Image/video/directory source.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Inference image size.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold before TCF.",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.7,
        help="NMS IoU threshold before TCF.",
    )
    parser.add_argument(
        "--tau",
        type=float,
        default=0.3,
        help="TCF host-defect IoU threshold.",
    )
    parser.add_argument(
        "--project",
        type=str,
        default="runs/detect",
        help="Output project directory.",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="tcf",
        help="Output experiment name.",
    )
    parser.add_argument(
        "--save-txt",
        action="store_true",
        help="Save filtered labels as txt files.",
    )
    parser.add_argument(
        "--hide-conf",
        action="store_true",
        help="Hide confidence scores in saved images.",
    )
    parser.add_argument(
        "--hide-labels",
        action="store_true",
        help="Hide class labels in saved images.",
    )

    return parser.parse_args()


def main() -> None:
    """Optional command-line inference entry."""
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise RuntimeError(
            "Please install ultralytics before running tcf.py as a script."
        ) from exc

    args = parse_args()

    save_dir = Path(args.project) / args.name
    image_dir = save_dir
    label_dir = save_dir / "labels"

    image_dir.mkdir(parents=True, exist_ok=True)

    if args.save_txt:
        label_dir.mkdir(parents=True, exist_ok=True)

    model = YOLO(args.model)

    results = model.predict(
        source=args.source,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        save=False,
        stream=False,
        verbose=True,
    )

    tcf = TargetConstrainedFilter(tau=args.tau)
    filtered_results, stats = tcf.filter_results(results, return_stats=True)

    total_removed = 0

    for r, st in zip(filtered_results, stats):
        total_removed += st.removed_defects

        stem = Path(getattr(r, "path", "result.jpg")).stem
        out_img = image_dir / f"{stem}.jpg"

        plotted = r.plot(
            conf=not args.hide_conf,
            labels=not args.hide_labels,
        )

        if cv2 is not None:
            cv2.imwrite(str(out_img), plotted)
        else:
            r.save(filename=str(out_img))

        if args.save_txt:
            save_yolo_txt(r, label_dir / f"{stem}.txt")

    print(f"TCF finished. Images saved to: {image_dir}")

    if args.save_txt:
        print(f"Filtered labels saved to: {label_dir}")

    print(f"Removed constrained defect predictions: {total_removed}")


if __name__ == "__main__":
    main()
