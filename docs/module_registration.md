# Module Registration

This document explains how to register the custom HSDNet modules in the Ultralytics YOLO framework.

---

## 1. Purpose

HSDNet is implemented based on the Ultralytics YOLO framework. This repository provides HSDNet-specific modified modules, model configuration files, scripts, and documentation.

This repository does **not** redistribute a complete modified Ultralytics source tree. Instead, the files in `models/` are provided as patch files and reference implementations. Users should install Ultralytics YOLO first and then merge or register the custom modules into their own compatible Ultralytics environment.

The required custom modules are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

In the manuscript, `SE_SPDConv` is described as **SE-SPDConv**. In source code and YAML configuration, `SE_SPDConv` is used because hyphens are not valid Python class names.

---

## 2. Source Files

The custom HSDNet modules are provided in the following files:

```text
models/block.py
models/head.py
models/tcf.py
```

These files should be regarded as HSDNet-specific patch files or reference implementations for integration with the Ultralytics YOLO framework.

The correspondence between paper-level names and code-level names is shown below.

| Paper-level name | Code-level class name | Source file | Function |
|---|---|---|---|
| SE-SPDConv | SE_SPDConv | `models/block.py` | Lightweight feature extraction |
| SplitOmniFusion | SplitOmniFusion | `models/block.py` | Multi-scale feature fusion |
| Detect_SEPS | Detect_SEPS | `models/head.py` | Detection head |
| Target-Constrained Filter | TCF | `models/tcf.py` | Post-processing / hierarchical defect filtering |

The files `models/block.py` and `models/head.py` may depend on other internal modules of the local Ultralytics environment. Therefore, users should merge the required custom classes into their own Ultralytics installation rather than treating these patch files as fully standalone modules.

---

## 3. Model Configuration

The model configuration file is:

```text
configs/hsdnet.yaml
```

The module names in `configs/hsdnet.yaml` should be consistent with the Python class names:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

Do not write the following name inside Python code or YAML configuration:

```text
SE-SPDConv
```

The hyphen in `SE-SPDConv` may cause parsing or identifier errors. Therefore, the paper-level name is written as `SE-SPDConv`, while the code-level name is written as `SE_SPDConv`.

---

## 4. Suggested Integration Procedure

Users can integrate the custom HSDNet modules into the Ultralytics YOLO framework using the following procedure:

1. Install the Ultralytics YOLO framework.
2. Locate the local Ultralytics installation directory.
3. Copy or merge the required custom classes from `models/block.py` into the corresponding Ultralytics module file for feature modules.
4. Copy or merge the required custom classes from `models/head.py` into the corresponding Ultralytics module file for detection heads.
5. Add the custom module imports to the relevant `__init__.py` file.
6. Make sure the Ultralytics model parsing function can access the custom module names.
7. Confirm that the module names in `configs/hsdnet.yaml` match the Python class names.
8. Apply `models/tcf.py` during inference or post-processing if TCF evaluation is required.
9. Run training, validation, or inference.

The required module names in the YAML configuration are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

---

## 5. Training Command

After the custom modules are registered, the model can be trained with:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=640 epochs=300 batch=24 device=0 optimizer=AdamW patience=30 workers=8
```

Alternatively, users can run:

```bash
python scripts/train.py
```

The default training settings used in this repository are consistent with the manuscript:

```text
image size: 640 × 640
epochs: 300
batch size: 24
optimizer: AdamW
patience: 30
workers: 8
```

---

## 6. Validation Command

After training, validation can be performed with:

```bash
yolo detect val model=runs/train/hsdnet/weights/best.pt data=configs/data_example.yaml imgsz=640 batch=24 device=0
```

Alternatively, users can run:

```bash
python scripts/val.py
```

---

## 7. Inference Command

Inference can be performed with:

```bash
yolo detect predict model=runs/train/hsdnet/weights/best.pt source=examples/images imgsz=640 device=0 save=True
```

Alternatively, users can run:

```bash
python scripts/predict.py
```

---

## 8. Target-Constrained Filter

The Target-Constrained Filter is implemented in:

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

When reporting TCF results, users should also discuss possible recall changes caused by missed host components.

---

## 9. Common Registration Errors

If one of the following errors occurs:

```text
KeyError: 'SE_SPDConv'
KeyError: 'SplitOmniFusion'
KeyError: 'Detect_SEPS'
ModuleNotFoundError
```

please check whether:

- the custom modules are defined in the source files;
- the custom modules are imported correctly;
- the module names in `configs/hsdnet.yaml` are consistent with the Python class names;
- the Ultralytics model parser can access the custom modules;
- the correct Python environment is being used;
- all required dependencies of the local Ultralytics environment are available.

---

## 10. Patch File Notice

This repository does not redistribute the full modified Ultralytics framework. The files in `models/` are provided as HSDNet-specific patch files. They document the modified modules used in the manuscript and should be integrated into a compatible Ultralytics YOLO codebase.

For full reproduction, users should ensure that their local Ultralytics environment contains all dependencies required by the custom modules.

---

## 11. Repository and Archive

GitHub repository:

```text
https://github.com/lshuang00001-ui/HSDNet
```

Archived version with DOI:

```text
https://doi.org/10.5281/zenodo.20065076
```
