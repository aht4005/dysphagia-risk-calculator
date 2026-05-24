import math
import streamlit as st

st.set_page_config(
    page_title="Post-Fundoplication Dysphagia Risk Calculator",
    page_icon="🩺",
    layout="centered"
)

st.title("Post-Fundoplication Dysphagia Risk Calculator")
st.markdown(
    "This research calculator estimates postoperative dysphagia risk after anti-reflux surgery "
    "using an interpretable point-based score derived from preoperative clinical and physiologic variables."
)

st.warning(
    "Research use only. This model has undergone internal validation but requires external/prospective validation "
    "before clinical deployment. It should not replace surgeon judgment."
)

with st.sidebar:
    st.header("Model inputs")
    age = st.number_input("Age at surgery", min_value=18.0, max_value=100.0, value=55.0, step=1.0)
    bmi = st.number_input("BMI", min_value=10.0, max_value=70.0, value=28.0, step=0.1)
    gerd_hrql = st.number_input("GERD-HRQL score", min_value=0.0, max_value=75.0, value=30.0, step=1.0)
    dci = st.number_input("Distal Contractile Integral / DCI", min_value=1.0, max_value=20000.0, value=1200.0, step=10.0)
    longest_reflux = st.number_input("Longest reflux episode on Bravo", min_value=1.0, max_value=10000.0, value=30.0, step=1.0)
    di = st.number_input("EndoFLIP Distensibility Index", min_value=0.01, max_value=20.0, value=2.0, step=0.01)
    les_pressure = st.number_input("LES pressure on HRM", min_value=0.0, max_value=200.0, value=20.0, step=0.1)
    mesh_use = st.selectbox("Mesh use", ["No", "Yes"])

mesh = 1 if mesh_use == "Yes" else 0

# Feature transformations
log_dci = math.log(dci)
log_reflux = math.log(longest_reflux)
log_di = math.log(di)

score = 0
components = []

def add_component(condition: bool, label: str, points: int, value: float, threshold: float):
    global score
    if condition:
        score += points
        components.append({
            "Component": label,
            "Value": round(value, 3),
            "Threshold": threshold,
            "Points": points
        })

add_component(log_dci * bmi >= 209.55, "log(DCI) × BMI", -9, log_dci * bmi, 209.55)
add_component(gerd_hrql * log_reflux >= 109.0, "GERD-HRQL × log(Longest reflux)", -3, gerd_hrql * log_reflux, 109.0)
add_component(age >= 61.52, "Age at surgery", -2, age, 61.52)
add_component(log_dci * mesh > 0, "log(DCI) × mesh use", 2, log_dci * mesh, 0.0)
add_component(log_reflux * age >= 207.29, "log(Longest reflux) × age", 2, log_reflux * age, 207.29)
add_component(log_di >= 1.02, "log(Distensibility Index)", 2, log_di, 1.02)
add_component(log_reflux * mesh > 0, "log(Longest reflux) × mesh use", 3, log_reflux * mesh, 0.0)
add_component(bmi * log_reflux >= 108.98, "BMI × log(Longest reflux)", 3, bmi * log_reflux, 108.98)
add_component(les_pressure * mesh > 0, "LES pressure × mesh use", 3, les_pressure * mesh, 0.0)
add_component(mesh == 1, "Mesh use", 4, mesh, 1.0)

st.subheader("Calculated result")
st.metric("Composite dysphagia risk score", score)

# IMPORTANT: Replace this cutoff with your final manuscript cutoff if different.
if score >= 0:
    st.error("Risk category: High risk")
else:
    st.success("Risk category: Low risk")

st.subheader("Score components triggered")
if components:
    st.dataframe(components, use_container_width=True, hide_index=True)
else:
    st.info("No scoring components were triggered for this input profile.")

st.subheader("Model details")
st.markdown(
    """
- Inputs include age, BMI, GERD-HRQL score, HRM-derived DCI and LES pressure, Bravo longest reflux episode, EndoFLIP distensibility index, and mesh use.  
- Continuous variables using logarithms are natural-log transformed.  
- The displayed cutoff is a placeholder based on the current scoring direction; replace it with the final manuscript-defined cutoff before publication.  
- Recommended citation: add manuscript/preprint DOI after publication.
    """
)
