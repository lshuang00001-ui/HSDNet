# Main Experimental Results

This file summarizes the main experimental results of HSDNet reported in the manuscript.

The experiments evaluate HSDNet from four aspects:

```text
overall detection performance
class-wise AP performance
edge deployment performance
cross-dataset generalization performance
```

---

## 1. Experimental Setting

The experiments were conducted on a self-built UAV transmission line inspection dataset.

The detection categories include:

```text
insulator
broken
flashover
hammer
corrode
nest
```

The main evaluation metrics are:

```text
Precision
Recall
mAP@0.5
mAP@0.5:0.95
Parameters
FLOPs
FPS
```

For fair comparison, all compared models were trained and evaluated under the same dataset split, training configuration, and testing protocol.

---

## 2. Overall Detection Performance

The comparison results of different detection models are shown below.

| Model | Layers | Params / M | FLOPs / G | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | FPS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| YOLOv8n | 168 | 3.00 | 8.1 | 0.8980 | 0.7980 | 0.8540 | 0.5300 | 224 |
| YOLOv11 | 238 | 2.58 | 6.3 | 0.8800 | 0.7850 | 0.8480 | 0.5240 | 384 |
| SCL-YOLOv11 | 277 | 1.70 | 4.3 | 0.8580 | 0.7710 | 0.8180 | 0.4490 | 322 |
| HSDNet | 235 | 2.80 | 10.5 | 0.9222 | 0.8604 | 0.8830 | 0.5707 | 198 |

---

## 3. Main Findings

Compared with YOLOv11, HSDNet achieves:

```text
mAP@0.5 improvement: +3.5 percentage points
mAP@0.5:0.95 improvement: +4.67 percentage points
Precision improvement: +4.22 percentage points
Recall improvement: +7.54 percentage points
```

Compared with YOLOv8n, HSDNet achieves:

```text
mAP@0.5 improvement: +2.9 percentage points
mAP@0.5:0.95 improvement: +4.07 percentage points
Precision improvement: +2.42 percentage points
Recall improvement: +6.24 percentage points
```

These results show that HSDNet improves both classification confidence and localization quality in UAV-based transmission line inspection scenarios.

Although HSDNet has higher FLOPs than some lightweight comparison models, it still maintains real-time inference capability with 198 FPS on the Windows platform.

---

## 4. Class-wise AP Results

The class-wise AP comparison between YOLOv11 and HSDNet is shown below.

| Model | insulator | broken | flashover | hammer | corrode | nest |
|---|---:|---:|---:|---:|---:|---:|
| YOLOv11 | 92.5 | 78.4 | 80.1 | 86.2 | 74.6 | 87.0 |
| HSDNet | 93.4 | 83.9 | 84.2 | 88.1 | 81.2 | 88.1 |

---

## 5. Class-wise Improvement

Compared with YOLOv11, HSDNet achieves the following AP improvements:

| Category | YOLOv11 AP | HSDNet AP | Improvement |
|---|---:|---:|---:|
| insulator | 92.5 | 93.4 | +0.9 |
| broken | 78.4 | 83.9 | +5.5 |
| flashover | 80.1 | 84.2 | +4.1 |
| hammer | 86.2 | 88.1 | +1.9 |
| corrode | 74.6 | 81.2 | +6.6 |
| nest | 87.0 | 88.1 | +1.1 |

The improvements are more obvious for defect-related categories, especially:

```text
broken
flashover
corrode
```

This indicates that the proposed modules are effective for small, weak-texture, and host-dependent defect targets.

---

## 6. Edge Deployment Performance

The deployment performance of HSDNet is summarized below.

| Metric | Result |
|---|---:|
| Windows platform single-model FPS | 198 |
| Linux edge-device stable FPS | 28 |
| Average end-to-end latency / ms | 33.7 |
| P95 latency / ms | 44.6 |
| Peak temperature / ℃ | 63.1 |
| Thermal throttling | No |
| Accuracy change after quantization / mAP@0.5 | No obvious decrease |

---

## 7. Deployment Analysis

The Windows-platform FPS reflects the single-model inference speed on a desktop environment.

The Linux edge-device FPS reflects the actual end-to-end detection throughput under onboard deployment conditions.

Therefore, the two FPS values should not be directly compared as absolute equivalents because they correspond to different hardware platforms and testing protocols.

The deployment results indicate that HSDNet can maintain real-time inference capability under edge deployment conditions.

---

## 8. Cross-dataset Generalization Results

To further evaluate generalization ability, HSDNet was tested on the external InsPLAD dataset.

| Model | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | F1 Score |
|---|---:|---:|---:|---:|---:|
| YOLOv11n | 86.7 | 75.6 | 82.2 | 45.8 | 80.8 |
| HSDNet | 89.7 | 83.3 | 87.0 | 51.7 | 86.4 |

---

## 9. Generalization Improvement

Compared with YOLOv11n on the external InsPLAD dataset, HSDNet achieves:

```text
Precision improvement: +3.0 percentage points
Recall improvement: +7.7 percentage points
mAP@0.5 improvement: +4.8 percentage points
mAP@0.5:0.95 improvement: +5.9 percentage points
F1 Score improvement: +5.6 percentage points
```

These results indicate that HSDNet has stronger cross-dataset robustness and better adaptability to complex UAV inspection scenes.

---

## 10. Summary

The main results show that HSDNet achieves a favorable balance between detection accuracy and deployment efficiency.

The key observations are:

```text
1. HSDNet achieves the best overall detection accuracy among the compared models.
2. HSDNet improves mAP@0.5 from 84.8% to 88.3% compared with the baseline.
3. HSDNet improves defect-related categories such as broken, flashover, and corrode.
4. HSDNet maintains real-time inference speed with 198 FPS on Windows.
5. HSDNet achieves approximately 28 FPS under Linux-based edge deployment.
6. HSDNet shows stronger generalization performance on the external InsPLAD dataset.
```

Overall, HSDNet improves detection accuracy, defect localization reliability, and edge deployment feasibility for UAV-based transmission line inspection.

---

## 11. Notes

The results in this file should be kept consistent with the final manuscript.

If the manuscript results are updated, the following values should be checked and revised accordingly:

```text
Precision
Recall
mAP@0.5
mAP@0.5:0.95
FPS
class-wise AP
deployment latency
generalization results
```