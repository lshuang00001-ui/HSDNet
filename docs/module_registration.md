# Module Registration

This document explains how to register the custom HSDNet modules in the Ultralytics YOLO framework.

## 1. Purpose

HSDNet is implemented based on the Ultralytics YOLO framework. This repository provides the modified HSDNet modules and configuration files, but users need to make sure that the custom modules are correctly recognized by the Ultralytics model parser before training.

The required custom modules are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

In the manuscript, `SE_SPDConv` is described as **SE-SPDConv**. In the source code and YAML configuration, `SE_SPDConv` is used because hyphens are not valid Python class names.

---

## 2. Source Files

The custom HSDNet modules are provided in the following files:

```text
models/block.py
models/head.py
models/tcf.py

These files should be regarded as HSDNet-specific patch files or reference implementations for integration with the Ultralytics YOLO framework.

Typical correspondence:

| Paper-level name          | Code-level class name | Source file     | Function                                        |
| ------------------------- | --------------------- | --------------- | ----------------------------------------------- |
| SE-SPDConv                | SE_SPDConv            | models/block.py | Lightweight feature extraction                  |
| SplitOmniFusion           | SplitOmniFusion       | models/block.py | Multi-scale feature fusion                      |
| Detect_SEPS               | Detect_SEPS           | models/head.py  | Detection head                                  |
| Target-Constrained Filter | TCF                   | models/tcf.py   | Post-processing / hierarchical defect filtering |


The files models/block.py and models/head.py may depend on other Ultralytics internal modules in the local environment. Therefore, users should merge the required custom classes into their own Ultralytics installation rather than importing these patch files as fully standalone modules.
```
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

because the hyphen may cause parsing or identifier errors.

---

## 4. Suggested Integration Procedure

Users can integrate the custom HSDNet modules into the Ultralytics YOLO framework using the following procedure:

1. Install the Ultralytics YOLO framework.
2. Locate the local Ultralytics installation directory.
3. Copy or merge the required custom classes from `models/block.py` into the corresponding Ultralytics module file for feature modules.
4. Copy or merge the required custom classes from `models/head.py` into the corresponding Ultralytics module file for detection heads.
5. Add the module imports to the relevant `__init__.py` file.
6. Make sure the Ultralytics model parsing function can access the custom module names.
7. Confirm that the module names in `configs/hsdnet.yaml` match the Python class names.
8. Apply `models/tcf.py` during inference or post-processing if TCF evaluation is required.
9. Run training or validation.

The required module names in the YAML configuration are:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS

---

## 5. Training Command

After registration, the model can be trained with:

```bash
yolo detect train model=configs/hsdnet.yaml data=configs/data_example.yaml imgsz=640 epochs=300 batch=24 device=0 optimizer=AdamW patience=30 workers=8
```

Alternatively, users can run:

```bash
python scripts/train.py
```

---

## 6. Validation Command

After training, validation can be performed with:

```bash
yolo detect val model=runs/train/hsdnet/weights/best.pt data=configs/data_example.yaml imgsz=640 device=0
```

Or:

```bash
python scripts/val.py
```

---

## 7. Common Errors

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
- the correct Python environment is being used.

---

## 8. Notes

This repository does not include the full Ultralytics YOLO source code. It provides the HSDNet-specific modified modules, configuration files, and reproduction instructions.

Users should first install the Ultralytics YOLO framework and then register the provided custom modules according to this document.

---

## 9. Patch File Notice

This repository does not redistribute the full modified Ultralytics framework. The files in `models/` are provided as HSDNet-specific patch files. They document the modified modules used in the manuscript and should be integrated into a compatible Ultralytics YOLO codebase.

For full reproduction, users should ensure that their local Ultralytics environment contains all dependencies required by the custom modules.
