import streamlit as st
import math

st.set_page_config(
    page_title="Dysphagia Risk Calculator",
    page_icon="🫁",
    layout="centered"
)

st.title("Post-Fundoplication Dysphagia Risk Calculator")
st.markdown(
    """
    This research-use calculator implements an interpretable point-based score for
    postoperative dysphagia risk after anti-reflux surgery.

    **Important:** Higher score = higher predicted dysphagia risk.
    Protective variables reduce the score.
    """
)

st.warning(
    "Research-use prototype only. This calculator is not externally/prospectively validated "
    "and should not replace clinical judgment."
)

st.header("Patient and Physiologic Inputs")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age at surgery (years)", min_value=18.0, max_value=100.0, value=55.0, step=1.0)
    bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=70.0, value=28.0, step=0.1)
    gerd_hrql = st.number_input("GERD-HRQL score", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    dci = st.number_input("Distal Contractile Integral (DCI)", min_value=0.01, value=1200.0, step=10.0)

with col2:
    longest_reflux = st.number_input("Longest reflux episode on Bravo", min_value=0.01, value=30.0, step=1.0)
    di = st.number_input("EndoFLIP Distensibility Index (DI)", min_value=0.01, value=2.0, step=0.01)
    les_pressure = st.number_input("LES pressure on HRM", min_value=0.0, value=20.0, step=0.1)
    mesh_use = st.selectbox("Mesh use", ["No", "Yes"])

mesh = 1 if mesh_use == "Yes" else 0

# Derived terms
log_dci = math.log(dci)
log_reflux = math.log(longest_reflux)
log_di = math.log(di)

score = 0
components = []

def add_component(condition, points, label):
    global score
    if condition:
        score += points
        components.append((label, points))

# Directionality rule:
# Higher score = higher dysphagia risk.
# OR > 1 terms add risk points.
# OR < 1 terms subtract/protective points.

# OR 2.490 -> risk
add_component(log_dci * bmi >= 209.55, +9, "log(DCI) × BMI ≥ 209.55")

# OR 1.708 -> risk
add_component(gerd_hrql * log_reflux >= 109.0, +3, "GERD-HRQL × log(Longest Reflux) ≥ 109")

# OR 0.595 -> protective
add_component(age >= 61.52, -2, "Age ≥ 61.52")

# OR 0.216 -> protective mesh interaction
add_component((log_dci * mesh) > 0, -2, "log(DCI) × Mesh Use > 0")

# OR 1.608 -> risk
add_component(log_reflux * age >= 207.29, +2, "log(Longest Reflux) × Age ≥ 207.29")

# OR 0.056 -> protective
add_component(log_di >= 1.02, -2, "log(DI) ≥ 1.02")

# OR 0.216 -> protective mesh interaction
add_component((log_reflux * mesh) > 0, -3, "log(Longest Reflux) × Mesh Use > 0")

# OR 3.893 -> risk
add_component(bmi * log_reflux >= 108.98, +3, "BMI × log(Longest Reflux) ≥ 108.98")

# OR 0.196 -> protective mesh interaction
add_component((les_pressure * mesh) > 0, -3, "LES Pressure × Mesh Use > 0")

# OR 0.216 -> protective
add_component(mesh == 1, -4, "Mesh Use = Yes")

st.divider()
st.header("Result")

st.metric("Total Dysphagia Risk Score", score)

# NOTE: This cutoff is a placeholder until the manuscript's final validated score threshold is confirmed.
# You should replace this with the final optimized cutoff from the validation cohort.
if score >= 0:
    st.error("Risk category: Higher risk")
else:
    st.success("Risk category: Lower risk")

st.caption(
    "Temporary classification cutoff used here: score ≥ 0 = higher risk. "
    "Replace with the final validated cutoff from the manuscript before publication."
)

with st.expander("Show score components"):
    if components:
        for label, pts in components:
            st.write(f"{label}: {pts:+d} points")
    else:
        st.write("No threshold components triggered.")

with st.expander("Derived log-transformed values"):
    st.write(f"log(DCI): {log_dci:.3f}")
    st.write(f"log(Longest Reflux): {log_reflux:.3f}")
    st.write(f"log(DI): {log_di:.3f}")

st.divider()
st.markdown(
    """
    **Open-source validation note:** Future versions may include an optional, IRB-approved,
    de-identified external validation registry. No user-entered data are stored in this prototype.
    """
)
