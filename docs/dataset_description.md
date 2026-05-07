# Dataset Description

This document describes the dataset format used for HSDNet.

## 1. Task Description

The task of this study is UAV-based transmission line defect detection. The model is trained to detect transmission line components and defect-related targets in UAV inspection images.

The example categories used in this repository are:

```text
insulator
broken
flashover
hammer
corrode
nest
```

These categories correspond to the example dataset configuration file:

```text
configs/data_example.yaml
```

If your manuscript uses a different number of categories, please modify both `configs/data_example.yaml` and `configs/hsdnet.yaml` accordingly.

---

## 2. Dataset Organization

The dataset should be organized in YOLO format.

The expected folder structure is:

```text
dataset
├── images
│   ├── train
│   ├── val
│   └── test
└── labels
    ├── train
    ├── val
    └── test
```

Each image should have a corresponding label file with the same file name.

For example:

```text
dataset/images/train/000001.jpg
dataset/labels/train/000001.txt
```

If the image name is:

```text
000001.jpg
```

then the label file should be:

```text
000001.txt
```

---

## 3. Annotation Format

Each label file follows the standard YOLO annotation format:

```text
class_id x_center y_center width height
```

where:

```text
class_id: category index
x_center: normalized x-coordinate of the bounding box center
y_center: normalized y-coordinate of the bounding box center
width: normalized width of the bounding box
height: normalized height of the bounding box
```

All coordinate values should be normalized to the range `[0, 1]`.

Example:

```text
0 0.5123 0.4381 0.0834 0.0625
1 0.6247 0.5129 0.0412 0.0386
```

This means the image contains two annotated targets.

---

## 4. Category Definition

The example category list is:

| Class ID | Category |
|---:|---|
| 0 | insulator |
| 1 | broken |
| 2 | flashover |
| 3 | hammer |
| 4 | corrode |
| 5 | nest |

The number of categories is:

```text
nc: 6
```

The category names should be consistent with the dataset configuration file.

---

## 5. Dataset Configuration

The dataset configuration file is:

```text
configs/data_example.yaml
```

A typical configuration is:

```yaml
path: dataset
train: images/train
val: images/val
test: images/test

nc: 6
names:
  - insulator
  - broken
  - flashover
  - hammer
  - corrode
  - nest
```

Before training, users should modify the `path` field according to their local dataset location.

For example, if the dataset is placed under the repository root, use:

```yaml
path: dataset
```

If the dataset is placed somewhere else, use the corresponding path.

---

## 6. Train/Validation/Test Split

The same dataset split should be used for all compared methods to ensure fair evaluation.

The recommended split structure is:

```text
images/train
images/val
images/test
labels/train
labels/val
labels/test
```

The training set is used for model training.

The validation set is used for model selection and performance evaluation during development.

The test set is used for final performance reporting if available.

---

## 7. Data Availability

The full UAV transmission line inspection dataset used in this study cannot be publicly released due to data ownership, privacy, and operational safety restrictions.

To support reproducibility, this repository provides:

```text
dataset organization format
YOLO annotation format
example category list
example dataset configuration
training and validation protocol
```

Access to the full dataset may be requested from the corresponding author for academic research purposes, subject to approval.