# Ablation Study Results

This file summarizes the ablation study results of HSDNet reported in the manuscript.

The ablation experiments are designed to evaluate the contribution of the following components:

```text
SE-SPDConv
SplitOmniFusion
Detect_SEPS
Target-Constrained Filter
Online Augmentation
```

---

## 1. Purpose of Ablation Study

The purpose of the ablation study is to verify whether each proposed module contributes to the final performance of HSDNet.

All ablation experiments are conducted under the same conditions, including:

```text
same dataset split
same input image size
same training epochs
same optimizer
same evaluation protocol
same post-processing settings unless otherwise specified
```

C2PSA is used as a default component in the baseline configuration and is therefore not separately removed in the ablation study.

---

## 2. Ablation Settings

The ablation variants are defined as follows:

| Number | Model Structure | Description |
|---|---|---|
| A0 | Baseline | Original baseline model |
| A1 | A0 + SE-SPDConv | Adds SE-SPDConv to improve lightweight spatial feature extraction |
| A2 | A1 + SplitOmniFusion | Adds SplitOmniFusion for multi-scale feature fusion |
| A3 | A2 + Detect_SEPS | Adds Detect_SEPS detection head |
| A4 | A3 + TCF | Adds Target-Constrained Filter |
| A4 + Aug | A4 + Online Aug | Adds online data augmentation during training |

---

## 3. Ablation Results

| Number | Model Structure | SE-SPDConv | SplitOmniFusion | Detect_SEPS | TCF | Online Aug | mAP@0.5 |
|---|---|---|---|---|---|---|---:|
| A0 | Baseline | × | × | × | × | × | 84.8 |
| A1 | A0 + SE-SPDConv | √ | × | × | × | × | 85.01 |
| A2 | A1 + SplitOmniFusion | √ | √ | × | × | × | 85.8 |
| A3 | A2 + Detect_SEPS | √ | √ | √ | × | × | 86.5 |
| A4 | A3 + TCF | √ | √ | √ | √ | × | 87.0 |
| A4 + Aug | A4 + Online Aug | √ | √ | √ | √ | √ | 88.3 |

---

## 4. Incremental Improvement

The incremental performance gain of each module is summarized below.

| Step | Added Component | mAP@0.5 Before | mAP@0.5 After | Improvement |
|---|---|---:|---:|---:|
| A0 → A1 | SE-SPDConv | 84.8 | 85.01 | +0.21 |
| A1 → A2 | SplitOmniFusion | 85.01 | 85.8 | +0.79 |
| A2 → A3 | Detect_SEPS | 85.8 | 86.5 | +0.70 |
| A3 → A4 | TCF | 86.5 | 87.0 | +0.50 |
| A4 → A4 + Aug | Online Augmentation | 87.0 | 88.3 | +1.30 |
| A0 → A4 + Aug | Full HSDNet | 84.8 | 88.3 | +3.50 |

---

## 5. Analysis of Each Module

### 5.1 SE-SPDConv

After introducing SE-SPDConv, the mAP@0.5 increases from 84.8% to 85.01%.

This indicates that SE-SPDConv can enhance small-target and weak-texture feature representation by preserving spatial information and recalibrating channel responses.

---

### 5.2 SplitOmniFusion

After introducing SplitOmniFusion, the mAP@0.5 increases from 85.01% to 85.8%.

This shows that SplitOmniFusion improves multi-scale feature fusion and helps the network better combine shallow detail information with deeper semantic information.

---

### 5.3 Detect_SEPS

After introducing Detect_SEPS, the mAP@0.5 increases from 85.8% to 86.5%.

This suggests that the shared enhanced detection head can improve classification and localization performance for multi-scale targets.

---

### 5.4 Target-Constrained Filter

After introducing TCF, the mAP@0.5 increases from 86.5% to 87.0%.

This indicates that modeling the spatial dependency between host components and defect targets can reduce invalid defect predictions and improve semantic consistency.

---

### 5.5 Online Augmentation

After adding online augmentation, the mAP@0.5 further increases from 87.0% to 88.3%.

This shows that online augmentation improves training sample diversity and helps the model adapt to UAV imaging variations such as illumination changes, blur, viewpoint changes, and background interference.

---

## 6. TCF Benefit-Cost Analysis

The Target-Constrained Filter is further evaluated by comparing the model before and after introducing TCF.

| Model | Broken AP | Flashover AP | Defect FPS | Defect Recall | Recall under Host Missed Detection |
|---|---:|---:|---:|---:|---:|
| A3 without TCF | 81.2 | 82.0 | 96 | 84.6 | 79.8 |
| A4 with TCF | 83.3 | 84.1 | 71 | 84.1 | 73.2 |

---

## 7. TCF Benefit-Cost Interpretation

After introducing TCF:

```text
Broken AP increases from 81.2 to 83.3.
Flashover AP increases from 82.0 to 84.1.
Defect false positives decrease from 96 to 71.
Defect recall slightly decreases from 84.6 to 84.1.
Recall under host missed detection decreases from 79.8 to 73.2.
```

These results indicate that TCF effectively suppresses false defect predictions that are not spatially associated with valid host components.

However, TCF also introduces a precision-recall trade-off. When the host component is missed, some true defect predictions may be filtered because no valid host target can be matched.

Therefore, TCF is more suitable for inspection scenarios where host components can be detected reliably.

---

## 8. TCF Threshold Sensitivity

The threshold sensitivity experiment evaluates the effect of different TCF overlap thresholds.

| Threshold τ | Precision | Recall | Broken AP | Flashover AP | Defect FPS |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 91.4 | 85.6 | 82.3 | 83.0 | 82 |
| 0.2 | 91.8 | 84.9 | 83.0 | 83.6 | 76 |
| 0.3 | 92.2 | 84.1 | 83.4 | 84.1 | 71 |
| 0.4 | 92.5 | 83.1 | 83.1 | 83.7 | 67 |
| 0.5 | 92.8 | 82.0 | 82.7 | 83.2 | 63 |

---

## 9. Threshold Selection

As the threshold τ increases, the constraint becomes stricter.

The observed trend is:

```text
Precision gradually increases.
Recall gradually decreases.
Defect FPS gradually decreases.
Broken AP and flashover AP reach a relatively balanced level around τ = 0.3.
```

When τ is too small, TCF is too loose and cannot sufficiently suppress background-induced false positives.

When τ is too large, TCF becomes too strict and may incorrectly filter true defect predictions.

Therefore, τ = 0.3 is selected as the default threshold because it provides a better balance among:

```text
defect detection accuracy
false positive suppression
recall preservation
semantic consistency
```

---

## 10. Summary

The ablation study verifies that each component contributes to the final performance of HSDNet.

The main conclusions are:

```text
1. SE-SPDConv improves spatial feature preservation and small-target representation.
2. SplitOmniFusion enhances multi-scale feature fusion.
3. Detect_SEPS improves classification and localization performance.
4. TCF suppresses semantically invalid defect predictions.
5. Online augmentation further improves robustness under UAV imaging variations.
6. The full HSDNet achieves 88.3% mAP@0.5, improving the baseline by 3.5 percentage points.
```

Overall, the results demonstrate that HSDNet improves detection accuracy through the combined effect of feature enhancement, multi-scale fusion, detection head optimization, hierarchical constraint, and training-time augmentation.

---

## 11. Notes

The values in this file should remain consistent with the final manuscript.

If the manuscript is revised, the following results should be checked and updated accordingly:

```text
ablation mAP@0.5
TCF benefit-cost results
TCF threshold sensitivity results
final selected TCF threshold
```