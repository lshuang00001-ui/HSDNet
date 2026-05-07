# Model Structure

This document summarizes the main structure of HSDNet.

## 1. Overview

HSDNet is a hierarchically constrained lightweight detection network for UAV-based transmission line defect detection and edge deployment.

The model is designed to address the following challenges in UAV inspection scenarios:

- small defect targets;
- weak texture and unclear boundaries;
- complex backgrounds;
- false positive detections;
- limited computing resources for edge deployment;
- spatial dependency between defect targets and host components.

The main components of HSDNet include:

```text
SE-SPDConv
SplitOmniFusion
Detect_SEPS
Target-Constrained Filter
```

In the source code and YAML configuration, **SE-SPDConv** is written as:

```text
SE_SPDConv
```

because hyphens are not valid Python class names.

---

## 2. Overall Framework

The general workflow of HSDNet can be summarized as:

```text
Input UAV image
        ↓
Backbone feature extraction
        ↓
SE-SPDConv-based lightweight feature enhancement
        ↓
SplitOmniFusion-based multi-scale feature fusion
        ↓
Detect_SEPS detection head
        ↓
Preliminary detection results
        ↓
Target-Constrained Filter
        ↓
Final detection results
```

The network aims to improve both detection accuracy and deployment efficiency.

---

## 3. SE-SPDConv

SE-SPDConv is used for lightweight feature extraction and spatial information preservation.

Its main purposes are:

- reducing spatial information loss during feature extraction;
- preserving fine-grained details of small targets;
- improving representation of weak-texture defect regions;
- maintaining a lightweight computational structure.

In the model configuration file, this module is written as:

```text
SE_SPDConv
```

Source file:

```text
models/block.py
```

---

## 4. SplitOmniFusion

SplitOmniFusion is designed for multi-scale feature interaction.

Its main purposes are:

- enhancing feature fusion across different scales;
- improving the representation of small and visually ambiguous defect targets;
- strengthening local and global feature interaction;
- improving detection robustness under complex backgrounds.

In the model configuration file, this module is written as:

```text
SplitOmniFusion
```

Source file:

```text
models/block.py
```

---

## 5. Detect_SEPS

Detect_SEPS is the detection head used in HSDNet.

Its main purposes are:

- improving classification performance;
- improving localization performance;
- supporting lightweight detection;
- enhancing detection stability for small defect targets.

In the model configuration file, this module is written as:

```text
Detect_SEPS
```

Source file:

```text
models/head.py
```

---

## 6. Target-Constrained Filter (TCF)

The Target-Constrained Filter (TCF) is a lightweight post-processing module used in HSDNet to model the hierarchical spatial relationship between host components and defect targets.

In transmission line inspection, some defect categories are not independent objects. Instead, they usually appear on, or near, specific host components. For example, defect categories such as `broken`, `flashover`, and `corrode` should normally be spatially associated with host components such as `insulator` or related structural parts. If such defects are predicted in irrelevant background regions, such as sky, tower edges, or isolated textures, the predictions are likely to be semantically invalid false positives.

Therefore, TCF introduces an explicit host-defect consistency check after the detector produces preliminary results. It does not modify the backbone, feature fusion module, or detection head, and it does not change the forward propagation path of the main network. Instead, it filters the final detection outputs according to whether each defect prediction has a valid spatial association with a corresponding host prediction.

The general workflow of TCF is:

```text
Preliminary detection results
        ↓
Separate host-object predictions and defect-object predictions
        ↓
For each defect prediction, calculate its spatial association with host boxes
        ↓
Retain the defect prediction if it satisfies the host-dependency constraint
        ↓
Remove isolated or semantically invalid defect predictions
        ↓
Final detection results
```

In the current task setting, the host-object category mainly corresponds to:

```text
insulator
```

The constrained defect categories mainly include:

```text
broken
flashover
corrode
```

For each predicted defect box, TCF calculates its overlap with the predicted host boxes. If the maximum overlap between the defect box and the host boxes is greater than a predefined threshold, the defect prediction is retained. Otherwise, the defect prediction is removed from the final output.

The default threshold used in the manuscript is:

```text
τ = 0.3
```

This threshold is not designed to enforce strict containment between a defect box and a host box. Instead, it only requires a reasonable spatial association. This is because real defect regions usually occupy only a small local area of the host component. An excessively strict threshold may incorrectly remove genuine small defects.

The main purposes of TCF are:

- suppressing isolated defect false positives in complex backgrounds;
- reducing semantically invalid predictions;
- improving the spatial consistency of defect detection results;
- reducing defect localization drift caused by background interference;
- enhancing the reliability of final inspection outputs.

TCF introduces a precision-recall trade-off. When the host component is correctly detected, TCF can effectively remove invalid defect predictions and improve result reliability. However, if the host component is missed, some true defect predictions may also be removed because no valid host association can be established. Therefore, the effectiveness of TCF depends partly on the detection reliability of host components.

In the ablation study, TCF should be evaluated by comparing two settings:

```text
without TCF
with TCF
```

Recommended evaluation indicators include:

```text
Precision
Recall
mAP@0.5
mAP@0.5:0.95
defect false positives
class-wise AP of defect categories
```

TCF is not a replacement for feature extraction or detection head optimization. It serves as an additional semantic consistency filtering mechanism that improves the rationality of final defect predictions by using the structural prior of transmission line inspection scenes.

---
## 7. Model Configuration

The model configuration file is:

```text
configs/hsdnet.yaml
```

The key module names in the YAML file should be:

```text
SE_SPDConv
SplitOmniFusion
Detect_SEPS
```

The paper-level and code-level names are:

| Paper-level name | Code-level name |
|---|---|
| SE-SPDConv | SE_SPDConv |
| SplitOmniFusion | SplitOmniFusion |
| Detect_SEPS | Detect_SEPS |
| Target-Constrained Filter | TCF |

---

## 8. Deployment-Oriented Design

HSDNet is designed for edge-oriented UAV inspection deployment.

The deployment evaluation should consider:

- detection accuracy;
- inference speed;
- number of parameters;
- FLOPs;
- model size;
- hardware platform;
- input image size;
- inference framework;
- precision mode.

When reporting deployment performance, the hardware and testing protocol should be clearly specified.

---

## 9. Notes

This repository provides the HSDNet-specific model configuration and modified modules.

Users should first install the Ultralytics YOLO framework and then register the custom modules according to:

```text
docs/module_registration.md
```

For step-by-step reproduction instructions, please refer to:

```text
docs/reproduction.md
```