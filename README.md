# HSDNet: Hierarchically Constrained Lightweight Network for UAV Transmission Line Defect Detection and Edge Deployment

[![DOI](https://zenodo.org/badge/1231611053.svg)](https://doi.org/10.5281/zenodo.20065075)

This repository provides the modified HSDNet modules, model configuration files, scripts, experimental result summaries, and reproducibility instructions for the manuscript:

**Hierarchically Constrained Lightweight Network for UAV Transmission Line Defect Detection and Edge Deployment**

HSDNet is designed for UAV-based transmission line defect detection under practical inspection scenarios. It focuses on lightweight visual detection, small-target representation, hierarchical defect constraint, and edge deployment efficiency.

---

## 1. Overview

UAV-based transmission line inspection is an important industrial visual computing task, but it faces several challenges:

- small and weak-texture defect targets;
- complex backgrounds and false positive responses;
- large appearance variations under UAV imaging conditions;
- limited computing resources for edge deployment;
- spatial dependency between defect targets and host components.

To address these problems, HSDNet introduces a lightweight detection framework with structural feature enhancement and hierarchical target constraints. The method aims to improve detection accuracy while maintaining real-time inference efficiency for practical inspection deployment.

---

## 2. Main Contributions

The main components of HSDNet include:

1. **SE-SPDConv-based lightweight feature extraction**  
   SE-SPDConv is used to preserve fine-grained spatial information while reducing computational redundancy.

2. **SplitOmniFusion for multi-scale feature interaction**  
   SplitOmniFusion enhances multi-scale feature representation for small and visually ambiguous defect targets.

3. **Detect_SEPS detection head**  
   Detect_SEPS is introduced to improve classification and localization performance under lightweight model constraints.

4. **Target-Constrained Filter (TCF)**  
   TCF imposes hierarchical spatial constraints between host components and defect targets, suppressing semantically invalid false detections in complex inspection scenes.

5. **Edge-oriented deployment evaluation**  
   The method is evaluated not only by detection accuracy but also by inference speed and deployment efficiency.

---

## 3. Repository Structure

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

## 4. Core Files

| File | Description |
|---|---|
| `configs/hsdnet.yaml` | Model configuration of HSDNet. |
| `configs/data_example.yaml` | Example dataset configuration in YOLO format. |
| `models/block.py` | HSDNet-specific patch file containing feature extraction and fusion modules, including SE_SPDConv and SplitOmniFusion-related implementations. |
| `models/head.py` | HSDNet-specific patch file containing Detect_SEPS and related detection head implementations. |
| `models/tcf.py` | Implementation of the Target-Constrained Filter for hierarchical defect suppression. |
| `scripts/train.py` | Training script. |
| `scripts/val.py` | Validation script. |
| `scripts/predict.py` | Inference script. |
| `docs/dataset_description.md` | Dataset description, category definitions, and annotation format. |
| `docs/reproduction.md` | Step-by-step reproduction instructions. |
| `docs/module_registration.md` | Instructions for registering custom HSDNet modules in the Ultralytics YOLO framework. |
| `docs/model_structure.md` | Description of the HSDNet model structure. |
| `results/main_results.md` | Main experimental results. |
| `results/ablation_results.md` | Ablation study results. |

---

## 5. Environment Requirements

The recommended environment is:

```text
Python >= 3.10
PyTorch >= 2.0
Ultralytics YOLO
CUDA-compatible GPU
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

Alternatively, create a conda environment:

```bash
conda create -n hsdnet python=3.10
conda activate hsdnet
pip install -r requirements.txt
```

Users can also create the environment using:

```bash
conda env create -f environment.yml
conda activate hsdnet
```

---

## 6. Important Note on Ultralytics Integration

This repository provides the modified HSDNet modules, model configuration files, scripts, and reproducibility instructions.

HSDNet is implemented based on the Ultralytics YOLO framework. This repository does **not** include the full Ultralytics source code. Instead, the files in `models/` are provided as HSDNet-specific patch files and reference implementations.

The custom modules required by HSDNet are provided in:

```text
models/block.py
models/head.py
models/tcf.py
```

The model configuration file is provided in:

```text
configs/hsdnet.yaml
```

Before training, users should first install the Ultralytics YOLO framework and then register or merge the provided custom modules into their local Ultralytics environment.

The required custom module names are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

The Target-Constrained Filter is implemented separately as a post-processing module:

```text
models/tcf.py
```

Detailed module registration instructions are provided in:

```text
docs/module_registration.md
```

Note that **SE-SPDConv** is the paper-level name, while **SE_SPDConv** is used as the code-level class name because hyphens are not valid in Python class names.

---

## 7. Dataset Preparation

The dataset should follow the standard YOLO detection format:

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

Each label file should follow the YOLO annotation format:

```text
class_id x_center y_center width height
```

All coordinates are normalized to the range `[0, 1]`.

An example dataset configuration is provided in:

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

If a different category set is used, modify `nc` and `names` accordingly.

---

## 8. Data Availability

The full UAV transmission line inspection dataset used in this study cannot be publicly released due to data ownership, privacy, and operational safety restrictions.

To support reproducibility, this repository provides:

- dataset organization format;
- YOLO annotation format;
- example dataset configuration;
- category definition instructions;
- training and validation protocol;
- reproduction instructions.

Access to the full dataset may be requested from the corresponding author for academic research purposes, subject to approval.

---

## 9. Training

Before training, modify:

```text
configs/data_example.yaml
```

to match the local dataset path.

Run:

```bash
python scripts/train.py
```

A typical training configuration used in the manuscript is:

```text
image size: 640 × 640
epochs: 300
batch size: 24
optimizer: AdamW
patience: 30
workers: 8
device: CUDA GPU
```

If using the Ultralytics command-line interface, the training command can be written as:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=640 epochs=300 batch=24 device=0 optimizer=AdamW patience=30 workers=8
```

---

## 10. Validation

Run validation using:

```bash
python scripts/val.py
```

Or use the Ultralytics command-line interface:

```bash
yolo detect val model=runs/train/hsdnet/weights/best.pt data=configs/data_example.yaml imgsz=640 batch=24 device=0
```

The main evaluation metrics include:

- Precision;
- Recall;
- mAP@0.5;
- mAP@0.5:0.95;
- Parameters;
- FLOPs;
- FPS.

---

## 11. Inference

Run inference on test images using:

```bash
python scripts/predict.py
```

Or use:

```bash
yolo detect predict model=runs/train/hsdnet/weights/best.pt source=examples/images imgsz=640 device=0 save=True
```

---

## 12. Target-Constrained Filter

The Target-Constrained Filter implementation is provided in:

```text
models/tcf.py
```

TCF is designed as a post-processing module. It does not change the main network architecture, feature extraction process, or detection head. Instead, it filters defect predictions according to the spatial dependency between host components and defect targets.

In the manuscript, TCF is used to suppress semantically invalid isolated defect predictions. For example, defect targets such as `broken`, `flashover`, and `corrode` should be spatially associated with valid host components.

A typical evaluation protocol for TCF includes two settings:

```text
without TCF
with TCF
```

Recommended indicators include:

```text
defect false positives
Precision
Recall
mAP@0.5
mAP@0.5:0.95
class-wise AP
qualitative detection examples
```

---

## 13. Reproducibility

To reproduce the main results:

1. Install the required environment.
2. Install the Ultralytics YOLO framework.
3. Register or merge the custom HSDNet modules according to `docs/module_registration.md`.
4. Prepare the dataset in YOLO format.
5. Modify `configs/data_example.yaml`.
6. Train HSDNet using `configs/hsdnet.yaml`.
7. Validate the trained model on the same validation or test split.
8. Compare the results with the reported metrics.

More detailed instructions are provided in:

```text
docs/reproduction.md
```

---

## 14. Experimental Results

The main results are summarized in:

```text
results/main_results.md
```

Ablation results are summarized in:

```text
results/ablation_results.md
```

In the manuscript, HSDNet achieves strong detection performance while maintaining efficient inference speed for edge deployment.

The reported main results include:

```text
mAP@0.5: 88.3%
Windows platform single-model FPS: 198
Linux edge-device stable FPS: approximately 28
```

---

## 15. Citation

If this repository is useful for your research, please cite the related manuscript and archived software release.

```bibtex
@article{HSDNet2026,
  title   = {Hierarchically Constrained Lightweight Network for UAV Transmission Line Defect Detection and Edge Deployment},
  author  = {Li, Min and Li, Shuang and Li, Kailong and Tong, Fengyu and Jiang, Zhenzhong and Zhao, Jinlu and Xu, Jining},
  journal = {The Visual Computer},
  year    = {2026}
}
```

Min Li and Shuang Li contributed equally to this work. Jining Xu is the corresponding author.

---

## 16. Code Availability

The source code, model configuration files, training scripts, validation scripts, inference scripts, Target-Constrained Filter implementation, experimental result summaries, and reproducibility instructions are publicly available in this repository.

GitHub repository:

```text
https://github.com/lshuang00001-ui/HSDNet
```

The archived version of this repository is available on Zenodo with a permanent DOI:

```text
https://doi.org/10.5281/zenodo.20065076
```

The DOI badge for the latest archived version is:

```markdown
[![DOI](https://zenodo.org/badge/1231611053.svg)](https://doi.org/10.5281/zenodo.20065075)
```

Please note that this repository provides the HSDNet-specific modified modules, configuration files, scripts, and documentation. Since HSDNet is implemented based on the Ultralytics YOLO framework, users should first install the Ultralytics YOLO framework and then register or merge the provided custom modules according to the instructions in:

```text
docs/module_registration.md
```

The full UAV transmission line inspection dataset used in the manuscript is not included in this repository due to data ownership, privacy, and operational safety restrictions. The dataset format, annotation protocol, category definitions, and example configuration file are provided for reproducibility.

---

## 17. License

This project follows the license statement provided in:

```text
LICENSE
```

Since this implementation is based on the Ultralytics YOLO framework, users should follow the license requirements of the corresponding Ultralytics YOLO version used in their environment.

---

## 18. Acknowledgement

This work is based on the Ultralytics YOLO framework and is developed for UAV-based transmission line defect detection and edge deployment research.

The authors thank the open-source community for providing useful tools and libraries for visual detection research.

---

## 19. Contact

For questions about the code, dataset format, or reproduction process, please contact the corresponding author.

```text
Corresponding author: Jining Xu
Email: jxu0422@ncut.edu.cn
```
