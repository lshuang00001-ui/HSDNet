# Reproduction Instructions

This document provides step-by-step instructions for reproducing the training, validation, inference, Target-Constrained Filter evaluation, and main experimental settings of HSDNet.

HSDNet is designed for UAV-based transmission line defect detection and edge deployment. The implementation is based on the Ultralytics YOLO framework.

---

## 1. Environment Setup

### 1.1 Recommended Environment

The recommended software environment is:

```text
Python >= 3.10
PyTorch >= 2.0
Ultralytics YOLO
CUDA-compatible GPU
Windows or Linux
```

The experiments in the manuscript were conducted using a CUDA-enabled GPU. CPU inference is supported, but GPU inference is recommended for training and speed evaluation.

---

### 1.2 Create Conda Environment

Create a new environment:

```bash
conda create -n hsdnet python=3.10
```

Activate the environment:

```bash
conda activate hsdnet
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, users can create the environment using:

```bash
conda env create -f environment.yml
conda activate hsdnet
```

---

## 2. Repository Structure

The expected repository structure is:

```text
HSDNet
│
├── README.md
├── requirements.txt
├── environment.yml
├── LICENSE
├── CITATION.cff
│
├── configs
│   ├── hsdnet.yaml
│   └── data_example.yaml
│
├── models
│   ├── __init__.py
│   ├── block.py
│   ├── head.py
│   └── tcf.py
│
├── scripts
│   ├── train.py
│   ├── val.py
│   └── predict.py
│
├── docs
│   ├── dataset_description.md
│   ├── reproduction.md
│   ├── module_registration.md
│   └── model_structure.md
│
└── results
    ├── main_results.md
    └── ablation_results.md
```

---

## 3. Dataset Preparation

### 3.1 Dataset Format

The dataset should be organized in YOLO detection format:

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

Each image should have a corresponding label file with the same base filename.

Example:

```text
dataset/images/train/000001.jpg
dataset/labels/train/000001.txt
```

---

### 3.2 Annotation Format

Each label file should follow the standard YOLO annotation format:

```text
class_id x_center y_center width height
```

All coordinates should be normalized to the range `[0, 1]`.

Example:

```text
0 0.5123 0.4381 0.0834 0.0625
1 0.6247 0.5129 0.0412 0.0386
```

---

### 3.3 Dataset Configuration

Modify the dataset configuration file:

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

The number of categories in `configs/data_example.yaml` must be consistent with the manuscript and with the trained model.

The example categories used in this repository are:

```text
insulator
broken
flashover
hammer
corrode
nest
```

---

## 4. Model Configuration

The model configuration file is:

```text
configs/hsdnet.yaml
```

The HSDNet configuration includes the following key modules:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

In the manuscript and documentation, `SE_SPDConv` may be described as **SE-SPDConv** for readability.

Note:

```text
SE-SPDConv is the paper-level name.
SE_SPDConv is the code-level class name.
```

Do not write `SE-SPDConv` inside Python class names or YAML module names, because the hyphen is not a valid Python identifier.

---

## 5. Ultralytics Integration

This repository provides HSDNet-specific patch files rather than a complete modified Ultralytics source tree.

The custom modules are provided in:

```text
models/block.py
models/head.py
models/tcf.py
```

Before training, users should register or merge the custom modules into a compatible Ultralytics YOLO environment.

The required module names are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

The TCF implementation is provided in:

```text
models/tcf.py
```

TCF can be applied to raw detection results during inference or post-processing.

Detailed module registration instructions are provided in:

```text
docs/module_registration.md
```

---

## 6. Training

### 6.1 Basic Training Command

Run:

```bash
python scripts/train.py
```

The default training script uses the following settings:

```text
model: configs/hsdnet.yaml
data: configs/data_example.yaml
image size: 640 × 640
epochs: 300
batch size: 24
optimizer: AdamW
patience: 30
workers: 8
device: 0
```

---

### 6.2 Training with Custom Arguments

For Windows PowerShell:

```bash
python scripts/train.py ^
  --model configs/hsdnet.yaml ^
  --data configs/data_example.yaml ^
  --imgsz 640 ^
  --epochs 300 ^
  --batch 24 ^
  --device 0 ^
  --optimizer AdamW ^
  --patience 30 ^
  --workers 8
```

For Linux or macOS:

```bash
python scripts/train.py \
  --model configs/hsdnet.yaml \
  --data configs/data_example.yaml \
  --imgsz 640 \
  --epochs 300 \
  --batch 24 \
  --device 0 \
  --optimizer AdamW \
  --patience 30 \
  --workers 8
```

---

### 6.3 Training with Ultralytics CLI

The model can also be trained using the Ultralytics command-line interface:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=640 epochs=300 batch=24 device=0 optimizer=AdamW patience=30 workers=8
```

---

### 6.4 Expected Output

After training, the results are usually saved in:

```text
runs/train/hsdnet
```

The trained weights are usually located at:

```text
runs/train/hsdnet/weights/best.pt
runs/train/hsdnet/weights/last.pt
```

---

## 7. Validation

### 7.1 Basic Validation Command

Run:

```bash
python scripts/val.py
```

---

### 7.2 Validation with Custom Arguments

For Windows PowerShell:

```bash
python scripts/val.py ^
  --weights runs/train/hsdnet/weights/best.pt ^
  --data configs/data_example.yaml ^
  --imgsz 640 ^
  --batch 24 ^
  --device 0 ^
  --split val
```

For Linux or macOS:

```bash
python scripts/val.py \
  --weights runs/train/hsdnet/weights/best.pt \
  --data configs/data_example.yaml \
  --imgsz 640 \
  --batch 24 \
  --device 0 \
  --split val
```

---

### 7.3 Validation with Ultralytics CLI

```bash
yolo detect val model=runs/train/hsdnet/weights/best.pt data=configs/data_example.yaml imgsz=640 batch=24 device=0
```

---

### 7.4 Evaluation Metrics

The main evaluation metrics include:

```text
Precision
Recall
mAP@0.5
mAP@0.5:0.95
Parameters
FLOPs
FPS
```

For fair comparison, all models should use the same dataset split, input image size, training configuration, and evaluation protocol.

---

## 8. Inference

### 8.1 Basic Inference Command

Run:

```bash
python scripts/predict.py
```

---

### 8.2 Inference with Custom Arguments

For Windows PowerShell:

```bash
python scripts/predict.py ^
  --weights runs/train/hsdnet/weights/best.pt ^
  --source examples/images ^
  --imgsz 640 ^
  --device 0 ^
  --conf 0.25 ^
  --iou 0.7
```

For Linux or macOS:

```bash
python scripts/predict.py \
  --weights runs/train/hsdnet/weights/best.pt \
  --source examples/images \
  --imgsz 640 \
  --device 0 \
  --conf 0.25 \
  --iou 0.7
```

---

### 8.3 Inference with Ultralytics CLI

```bash
yolo detect predict model=runs/train/hsdnet/weights/best.pt source=examples/images imgsz=640 device=0 save=True
```

The inference results are usually saved in:

```text
runs/predict/hsdnet
```

or:

```text
runs/detect/predict
```

depending on the Ultralytics version and script configuration.

---

## 9. FPS Reporting

This repository does not provide a standalone FPS evaluation script. Inference speed can be evaluated using the Ultralytics prediction interface or a user-defined timing script.

When reporting FPS, specify the following information:

```text
hardware platform
GPU or edge device type
CPU type
input image size
batch size
inference framework
precision mode
number of warm-up iterations
number of test iterations
```

The manuscript reports the following deployment performance:

```text
Windows platform single-model FPS: 198
Linux edge-device stable FPS: approximately 28
Average end-to-end latency: 33.7 ms
P95 latency: 44.6 ms
```

The Windows FPS and Linux edge-device FPS correspond to different hardware platforms and testing protocols, so they should not be directly compared as absolute equivalents.

---

## 10. Reproducing Main Results

To reproduce the main results reported in the manuscript:

1. Install the required environment.
2. Install the Ultralytics YOLO framework.
3. Register or merge the custom HSDNet modules according to `docs/module_registration.md`.
4. Prepare the dataset in YOLO format.
5. Modify `configs/data_example.yaml`.
6. Confirm that `configs/hsdnet.yaml` uses the correct custom module names.
7. Train HSDNet using the same training settings.
8. Validate the best checkpoint on the same validation or test set.
9. Record the metrics.
10. Compare the results with `results/main_results.md`.

Recommended training settings:

```text
imgsz = 640
epochs = 300
batch = 24
optimizer = AdamW
patience = 30
workers = 8
device = 0
```

---

## 11. Reproducing Ablation Studies

To reproduce ablation studies, train different model variants under the same experimental settings.

Typical ablation variants include:

```text
Baseline
Baseline + SE-SPDConv
Baseline + SE-SPDConv + SplitOmniFusion
Baseline + SE-SPDConv + SplitOmniFusion + Detect_SEPS
Baseline + SE-SPDConv + SplitOmniFusion + Detect_SEPS + TCF
Full HSDNet with Online Augmentation
```

All variants should use:

```text
same dataset split
same image size
same number of epochs
same optimizer
same batch size
same patience setting
same evaluation protocol
```

The ablation results are summarized in:

```text
results/ablation_results.md
```

---

## 12. Target-Constrained Filter Evaluation

The TCF implementation is provided in:

```text
models/tcf.py
```

The Target-Constrained Filter can be applied to the raw detection results during inference or post-processing.

If TCF is implemented as an additional inference or post-processing module, evaluate it using two settings:

```text
without TCF
with TCF
```

Recommended evaluation indicators include:

```text
defect false positives
Precision
Recall
mAP@0.5
mAP@0.5:0.95
class-wise AP
qualitative detection examples
```

TCF is designed to suppress semantically invalid isolated defect predictions by modeling the spatial dependency between host components and defect targets.

When reporting TCF results, also discuss possible recall changes caused by missed host components.

---

## 13. Notes on Reproducibility

The exact numerical results may vary slightly due to:

```text
GPU type
CUDA version
PyTorch version
Ultralytics version
random seed
data loading order
training precision
hardware-specific acceleration
```

For fair comparison, use the same environment, dataset split, and training settings for all compared methods.

---

## 14. Common Errors

### 14.1 Module Not Found

If an error similar to the following appears:

```text
KeyError: 'SE_SPDConv'
KeyError: 'SplitOmniFusion'
KeyError: 'Detect_SEPS'
ModuleNotFoundError
```

check whether the custom modules are correctly defined, imported, and registered in the Ultralytics parsing system.

The module names in `configs/hsdnet.yaml` must match the class names in the source code.

---

### 14.2 Dataset Path Error

If an error indicates that images or labels cannot be found, check:

```text
configs/data_example.yaml
```

Make sure the dataset path is correct.

Example:

```yaml
path: dataset
train: images/train
val: images/val
test: images/test
```

---

### 14.3 CUDA Out of Memory

If CUDA memory is insufficient, reduce the batch size:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=640 epochs=300 batch=12 device=0 optimizer=AdamW patience=30 workers=8
```

If the problem remains, reduce the input size:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=512 epochs=300 batch=12 device=0 optimizer=AdamW patience=30 workers=8
```

---

### 14.4 Weight File Not Found

If the validation or inference script cannot find the model weights, check whether the path exists:

```text
runs/train/hsdnet/weights/best.pt
```

or modify the script argument:

```bash
python scripts/val.py --weights path/to/best.pt
```

---

## 15. Data Availability Statement

The full UAV transmission line inspection dataset cannot be publicly released due to data ownership, privacy, and operational safety restrictions.

To support reproducibility, this repository provides:

```text
dataset organization format
annotation format
category definition instructions
training protocol
validation protocol
example configuration file
```

Access to the full dataset may be requested from the corresponding author for academic research purposes, subject to approval.

---

## 16. Code Availability Statement

The source code, model configuration files, training scripts, validation scripts, inference scripts, Target-Constrained Filter implementation, experimental result summaries, and reproduction instructions are publicly available in this repository.

GitHub repository:

```text
https://github.com/lshuang00001-ui/HSDNet
```

Archived version with permanent DOI:

```text
https://doi.org/10.5281/zenodo.20066405
```

Please note that this repository provides the HSDNet-specific modified modules, configuration files, scripts, and documentation. Since HSDNet is implemented based on the Ultralytics YOLO framework, users should first install the Ultralytics YOLO framework and then register or merge the provided custom modules according to the instructions in:

```text
docs/module_registration.md
```

The full UAV transmission line inspection dataset used in the manuscript is not included in this repository due to data ownership, privacy, and operational safety restrictions. The dataset format, annotation protocol, category definitions, and example configuration file are provided for reproducibility.

---

## 17. Contact

For questions about reproduction, dataset format, model implementation, or code usage, please contact the repository maintainer or the corresponding author of the related manuscript.

```text
Repository maintainer: Shuang Li
Email: lishuang@mail.ncut.edu.cn

Corresponding author: Jining Xu
Email: jxu0422@ncut.edu.cn
