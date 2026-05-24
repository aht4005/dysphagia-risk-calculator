# Post-Fundoplication Dysphagia Risk Calculator

Open-source research calculator for estimating postoperative dysphagia risk after anti-reflux surgery using a point-based score derived from preoperative clinical and physiologic variables.

## Inputs
- Age at surgery
- BMI
- GERD-HRQL score
- Distal Contractile Integral (DCI)
- Longest reflux episode on Bravo
- EndoFLIP Distensibility Index
- LES pressure on HRM
- Mesh use

## Output
- Composite dysphagia risk score
- Low-risk vs high-risk category
- Triggered score components

## Disclaimer
This calculator is for research use only. It has not yet undergone external or prospective validation and should not replace clinical judgment.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
