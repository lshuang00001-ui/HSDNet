import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Run inference with HSDNet.")

    parser.add_argument(
        "--weights",
        type=str,
        default="runs/train/hsdnet/weights/best.pt",
        help="Path to trained HSDNet weights."
    )
    parser.add_argument(
        "--source",
        type=str,
        default="examples/images",
        help="Path to input image, folder, video, or camera source."
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size for inference."
    )
    parser.add_argument(
        "--device",
        type=str,
        default="0",
        help="CUDA device id, such as 0, or cpu."
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold."
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.7,
        help="IoU threshold for NMS."
    )
    parser.add_argument(
        "--project",
        type=str,
        default="runs/predict",
        help="Directory for saving prediction results."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="hsdnet",
        help="Name of prediction run."
    )
    parser.add_argument(
        "--save",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Save prediction results."
    )

    return parser.parse_args()


def resolve_path(path_str):
    """
    Resolve relative paths from the repository root.
    This allows the script to be executed from the repository root.
    """
    repo_root = Path(__file__).resolve().parents[1]
    path = Path(path_str)

    if path.is_absolute():
        return str(path)

    return str(repo_root / path)


def main():
    args = parse_args()

    weights = resolve_path(args.weights)

    source_path = Path(args.source)
    if source_path.is_absolute():
        source = str(source_path)
    else:
        source = str(Path(__file__).resolve().parents[1] / source_path)

    model = YOLO(weights)

    model.predict(
        source=source,
        imgsz=args.imgsz,
        device=args.device,
        conf=args.conf,
        iou=args.iou,
        project=args.project,
        name=args.name,
        save=args.save,
    )


if __name__ == "__main__":
    main()