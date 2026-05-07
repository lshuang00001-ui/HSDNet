import argparse
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Train HSDNet.")

    parser.add_argument(
        "--model",
        type=str,
        default="configs/hsdnet.yaml",
        help="Path to HSDNet model configuration."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="configs/data_example.yaml",
        help="Path to dataset configuration."
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch", type=int, default=24)
    parser.add_argument("--device", type=str, default="0")
    parser.add_argument("--optimizer", type=str, default="AdamW")
    parser.add_argument("--patience", type=int, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--project", type=str, default="runs/train")
    parser.add_argument("--name", type=str, default="hsdnet")

    return parser.parse_args()


def main():
    args = parse_args()

    model = YOLO(args.model)

    model.train(
        data=args.data,
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        device=args.device,
        optimizer=args.optimizer,
        patience=args.patience,
        workers=args.workers,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()