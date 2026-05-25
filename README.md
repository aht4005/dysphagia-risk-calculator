[README.md](https://github.com/user-attachments/files/28201582/README.md)
# Post-Fundoplication Dysphagia Risk Calculator

Open-source research-use prototype implementing an interpretable point-based risk score for postoperative dysphagia after anti-reflux surgery.

## What this calculator does

The calculator uses preoperative and perioperative variables including:

- Age
- BMI
- GERD-HRQL score
- Distal Contractile Integral (DCI)
- Longest reflux episode on Bravo testing
- EndoFLIP Distensibility Index
- LES pressure
- Mesh use

It outputs an interpretable dysphagia risk score.

## Score direction

**Higher score = higher predicted dysphagia risk.**

Variables with odds ratios greater than 1 increase the score.  
Variables with odds ratios less than 1 are treated as protective and decrease the score.

## Important disclaimer

This calculator is a research-use prototype only.  
It has not yet undergone external or prospective validation and should not replace clinical judgment.

## Citation

Manuscript currently under review.
