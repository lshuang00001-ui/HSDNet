# HSDNet: Hierarchically Constrained Lightweight Network for UAV Transmission Line Defect Detection and Edge Deployment

This repository provides the modified HSDNet modules, model configuration files, and reproducibility instructions for the manuscript:

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
HSDNet_release
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
│   ├── block.py
│   ├── head.py
│   └── __init__.py
│
├── scripts
│   ├── train.py
│   ├── val.py
│   ├── predict.py
│
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
| `scripts/get_fps.py` | Inference speed evaluation script. |
| `docs/dataset_description.md` | Dataset description, category definitions, and annotation format. |
| `docs/reproduction.md` | Step-by-step reproduction instructions. |
| `docs/module_registration.md` | Instructions for registering custom HSDNet modules in the Ultralytics YOLO framework. |
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

---

## 6. Important Note on Ultralytics Integration

This repository provides the modified HSDNet modules, model configuration files, scripts, and reproducibility instructions.

HSDNet is implemented based on the Ultralytics YOLO framework. This repository does not include the full Ultralytics source code. Instead, the files in `models/` are provided as HSDNet-specific patch files and reference implementations.

Specifically, the custom modules required by HSDNet are provided in:

```text
models/block.py
models/head.py
models/tcf.py

The model configuration file is provided in:
configs/hsdnet.yaml

Before training, users should first install the Ultralytics YOLO framework and then register or merge the provided custom modules into their local Ultralytics environment.

The required custom module names are:

SE_SPDConv
SplitOmniFusion
Detect_SEPS

The Target-Constrained Filter is implemented separately as a post-processing module:
models/tcf.py

Detailed module registration instructions are provided in:
docs/module_registration.md

Note that SE-SPDConv is the paper-level name, while SE_SPDConv is used as the code-level class name because hyphens are not valid in Python class names.

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

where all coordinates are normalized to the range `[0, 1]`.

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

Then run:

```bash
python scripts/train.py
```

A typical training configuration used in the manuscript is:

```text
image size: 640 × 640
epochs: 300
batch size: 24
optimizer: AdamW
initial learning rate: 0.01
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
yolo detect val model=runs/train/hsdnet/weights/best.pt data=configs/data_example.yaml imgsz=640 device=0
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

## 12. Inference Speed Evaluation

To evaluate inference speed:

```bash
python scripts/get_fps.py
```

When reporting FPS, please specify:

- hardware platform;
- GPU or edge device type;
- input image size;
- batch size;
- inference framework;
- precision mode, such as FP32, FP16, or TensorRT;
- number of warm-up iterations;
- number of test iterations.

---

## 13. Reproducibility

To reproduce the main results:

1. Install the required environment.
2. Install the Ultralytics YOLO framework.
3. Register the custom HSDNet modules according to `docs/module_registration.md`.
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

---

## 15. Code Availability

The source code, configuration files, training scripts, inference scripts, and reproducibility instructions are available in this repository.

A permanent archived version will be provided through Zenodo after the official GitHub release.

```text
GitHub repository: https://github.com/your_username/HSDNet
Zenodo DOI: https://doi.org/10.5281/zenodo.xxxxxxxx
```

Please replace the above links after creating the GitHub repository and Zenodo archive.

---

## 16. Citation

If this repository is useful for your research, please cite the related manuscript:

```bibtex
@article{HSDNet2026,
  title   = {Hierarchically Constrained Lightweight Network for UAV Transmission Line Defect Detection and Edge Deployment},
  author  = {Author Name and Author Name and Author Name},
  journal = {The Visual Computer},
  year    = {2026}
}
```

After publication, the citation information will be updated.

---

## 17. License

This project is released for academic research purposes.

Since this implementation is based on the Ultralytics YOLO framework, please follow the license requirements of the corresponding Ultralytics version used in this repository.

If the implementation directly modifies or redistributes Ultralytics source code, please ensure that the license file is consistent with the original framework license.

---

## 18. Acknowledgement

This work is based on the Ultralytics YOLO framework and is developed for UAV-based transmission line defect detection and edge deployment research.

The authors thank the open-source community for providing useful tools and libraries for visual detection research.

---

## 19. Contact

For questions about the code, dataset format, or reproduction process, please contact:

```text
Corresponding author: Jining Xu
Email: jxu0422@ncut.edu.cn
```

Please replace the contact information before releasing the repository.