import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Validate HSDNet.")

    parser.add_argument(
        "--weights",
        type=str,
        default="runs/train/hsdnet/weights/best.pt",
        help="Path to trained HSDNet weights."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="configs/data_example.yaml",
        help="Path to dataset configuration file."
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size for validation."
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=24,
        help="Batch size for validation."
    )
    parser.add_argument(
        "--device",
        type=str,
        default="0",
        help="CUDA device id, such as 0, or cpu."
    )
    parser.add_argument(
        "--split",
        type=str,
        default="val",
        choices=["train", "val", "test"],
        help="Dataset split used for validation."
    )
    parser.add_argument(
        "--project",
        type=str,
        default="runs/val",
        help="Directory for saving validation results."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="hsdnet",
        help="Name of validation run."
    )
    parser.add_argument(
        "--save_json",
        action="store_true",
        help="Save validation results in JSON format."
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
    data = resolve_path(args.data)

    model = YOLO(weights)

    model.val(
        data=data,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        split=args.split,
        project=args.project,
        name=args.name,
        save_json=args.save_json,
    )


if __name__ == "__main__":
    main()