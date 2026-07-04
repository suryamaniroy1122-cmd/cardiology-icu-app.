import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Advanced Cardiology ICU Monitor", page_icon="🏥", layout="wide")
st.title("🏥 Clinical Cardiology Integrated ICU Dashboard")
st.subheader("Advanced Hemodynamics & Telemetry Engineering Platform")

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Timestamp", "Heart Rate", "MAP", "SpO2", "Ejection Fraction", "Cardiac Output"])
if "active_meds" not in st.session_state:
    st.session_state.active_meds = []

st.sidebar.header("🎛️ Live Telemetry Controls")
input_hr = st.sidebar.slider("Heart Rate (bpm)", 40, 180, 115)
input_sys = st.sidebar.slider("Systolic BP (mmHg)", 70, 200, 155)
input_dia = st.sidebar.slider("Diastolic BP (mmHg)", 40, 120, 95)
input_spo2 = st.sidebar.slider("Oxygen Saturation (SpO2 %)", 70, 100, 89)

st.sidebar.markdown("---")
st.sidebar.header("💉 ICU Clinical Interventions")

if st.sidebar.button("Administer Metoprolol (Beta-Blocker)"):
    if "Beta-Blocker" not in st.session_state.active_meds: st.session_state.active_meds.append("Beta-Blocker")
if st.sidebar.button("Deploy Dobutamine (Inotrope)"):
    if "Inotrope" not in st.session_state.active_meds: st.session_state.active_meds.append("Inotrope")
if st.sidebar.button("Deploy Supplemental Oxygen"):
    if "Oxygen Therapy" not in st.session_state.active_meds: st.session_state.active_meds.append("Oxygen Therapy")
if st.sidebar.button("Reset / Clear All Supports"):
    st.session_state.active_meds = []

current_hr = int(input_hr * 0.75) if "Beta-Blocker" in st.session_state.active_meds else input_hr
current_hr = int(current_hr * 1.05) if "Inotrope" in st.session_state.active_meds else current_hr
current_sys = int(input_sys * 0.88) if "Beta-Blocker" in st.session_state.active_meds else input_sys
current_dia = int(input_dia * 0.88) if "Beta-Blocker" in st.session_state.active_meds else input_dia
current_spo2 = min(100, input_spo2 + 8) if "Oxygen Therapy" in st.session_state.active_meds else input_spo2

map_val = int((current_sys + (2 * current_dia)) / 3)
edv, esv = 120, 50
if "Inotrope" in st.session_state.active_meds: esv = int(esv * 0.6)

sv = edv - esv
ef = round((sv / edv) * 100, 1)
co = round((current_hr * sv) / 1000, 2)

new_entry = pd.DataFrame([{"Timestamp": time.strftime("%H:%M:%S"), "Heart Rate": current_hr, "MAP": map_val, "SpO2": current_spo2, "Ejection Fraction": ef, "Cardiac Output": co}])
st.session_state.history = pd.concat([st.session_state.history, new_entry], ignore_index=True).tail(15)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="♥️ Heart Rate", value=f"{current_hr} bpm")
    st.metric(label="🫀 Ejection Fraction (EF)", value=f"{ef} %")
with col2:
    st.metric(label="📈 Mean Arterial Pressure (MAP)", value=f"{map_val} mmHg", delta=f"BP: {current_sys}/{current_dia}")
    st.metric(label="🧪 Cardiac Output (CO)", value=f"{co} L/min")
with col3:
    st.metric(label="🫁 Oxygen Saturation (SpO2)", value=f"{current_spo2} %")

st.markdown("### 🧪 Active Medical Support Pipelines")
if st.session_state.active_meds: st.success(f"Running Infusions: {', '.join(st.session_state.active_meds)}")
else: st.info("Patient maintaining baseline native circulation (No active supports).")

st.markdown("### 🚨 Safety Monitoring Node")
alerts = []
if map_val < 65: alerts.append("⚠️ CRITICAL ALERT: Circulatory Shock Detected (MAP < 65 mmHg)")
if current_spo2 < 90: alerts.append("⚠️ CRITICAL ALERT: Severe Hypoxemia Detected (SpO2 < 90%)")
if ef < 40: alerts.append("⚠️ CRITICAL ALERT: Myocardial Depression / Heart Failure State")

if alerts:
    for alert in alerts: st.error(alert)
else: st.success("✅ Telemetry Metrics within Safe Parameter Boundaries.")

st.markdown("---")
st.markdown("### 📊 Real-Time Patient Vitals Trend Chart")
st.line_chart(st.session_state.history.set_index("Timestamp"))
