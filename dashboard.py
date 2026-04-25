"""
Terminal Dashboard / Web UI
===========================
Streamlit implementation for a polished, beginner-friendly 
flight safety monitoring interface.
"""

import os
import time
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import main

# Page Configuration
st.set_page_config(
    page_title="Flight Safety Monitor & XAI", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
BASE_DIR = Path(__file__).resolve().parent
ALERTS_CSV = BASE_DIR / "outputs" / "alerts_output.csv"

# Custom CSS for polished layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .header-box {
        background: linear-gradient(135deg, rgba(15, 32, 55, 0.8) 0%, rgba(5, 14, 23, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 25px 30px;
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.05);
        color: white;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .header-box::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.05), transparent);
        transform: skewX(-20deg); animation: shine 6s infinite;
    }
    @keyframes shine { 0% {left: -100%;} 20% {left: 200%;} 100% {left: 200%;} }
    
    .header-title { font-size: 36px; font-weight: 800; margin:0; background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .header-subtitle { font-size: 16px; color: #94a3b8; margin-top:5px; font-weight: 300; letter-spacing: 0.5px; }
    
    .metric-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 20px 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.05);
        border-bottom: 3px solid #3b82f6;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        border-bottom: 3px solid #60a5fa;
    }
    .metric-value { font-size: 30px; font-weight: 800; margin: 10px 0; color: #f8fafc; text-shadow: 0 2px 10px rgba(255,255,255,0.1); }
    .metric-label { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    
    .risk-badge {
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 13px;
        display: inline-block;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .risk-badge:hover { transform: scale(1.05); }
    .risk-CRITICAL { background: linear-gradient(135deg, #ef4444, #991b1b); color: white; border: 1px solid #f87171; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
    .risk-WARNING { background: linear-gradient(135deg, #f59e0b, #b45309); color: white; border: 1px solid #fbbf24; box-shadow: 0 0 15px rgba(245, 158, 11, 0.4); }
    .risk-STABLE { background: linear-gradient(135deg, #10b981, #047857); color: white; border: 1px solid #34d399; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
    .risk-HIGH { background: linear-gradient(135deg, #ef4444, #991b1b); color: white; border: 1px solid #f87171; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
    .risk-NORMAL { background: linear-gradient(135deg, #10b981, #047857); color: white; border: 1px solid #34d399; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
    .risk-ANOMALY { background: linear-gradient(135deg, #8b5cf6, #5b21b6); color: white; border: 1px solid #a78bfa; box-shadow: 0 0 15px rgba(139, 92, 246, 0.4); }
    
    .xai-box, .advisory-box {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 12px;
        color: #f8fafc;
        margin-top: 15px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        line-height: 1.5;
    }
    .xai-box { border-left: 4px solid #8b5cf6; }
    .advisory-box { border-left: 4px solid #ef4444; font-weight: 600; }
    .xai-box:hover { border-left-width: 8px; background: rgba(30, 41, 59, 0.8); }
    .advisory-box:hover { border-left-width: 8px; background: rgba(30, 41, 59, 0.8); }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data():
    if not ALERTS_CSV.exists():
        return None
    return pd.read_csv(ALERTS_CSV)

st.markdown("""
<div class="header-box">
    <p class="header-title">✈️ Agentic AI-Based Flight Safety Monitoring System</p>
    <p class="header-subtitle">Real-time Anomaly Prediction & Explainable AI (XAI) Digital Co-Pilot</p>
</div>
""", unsafe_allow_html=True)

with st.expander("📁 Upload Custom Flight Data", expanded=False):
    st.markdown("Upload a CSV containing flight telemetry parameters (`altitude`, `speed`, `engine_temp`, `wind_speed`, `vibration`, `fuel_flow`, `cabin_pressure`). The system will run the AI agents and generate a new safety report.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        if st.button("Run AI Analysis"):
            with st.spinner("Analyzing telemetry with multi-agent system..."):
                upload_path = BASE_DIR / "data" / "uploaded_flight_data.csv"
                with open(upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                try:
                    main.run_simulation(str(upload_path), str(ALERTS_CSV))
                    st.success("Analysis complete! Reloading dashboard...")
                    time.sleep(1)
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

df = load_data()

if df is None:
    st.error(f"No output data found at {ALERTS_CSV}. Please run `python generate_data.py` and `python main.py` first.")
    st.stop()

# Auto Refresh mechanics to simulate streaming
if 'tick' not in st.session_state:
    st.session_state.tick = len(df)

# Use the full dataframe
df_view = df
current = df_view.iloc[-1]

# ----------------- UI ROW 1: TELEMETRY -----------------
st.markdown("### 📡 Live Sensor Telemetry")
m1, m2, m3, m4, m5, m6 = st.columns(6)
def make_metric(col, label, value, unit=""):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}{unit}</div></div>', unsafe_allow_html=True)

make_metric(m1, "Altitude", f"{current['altitude']:,.0f}", " ft")
make_metric(m2, "Speed", f"{current['speed']:.0f}", " kts")
make_metric(m3, "Engine Temp", f"{current['engine_temp']:.0f}", " °C")
make_metric(m4, "Wind Speed", f"{current['wind_speed']:.0f}", " kts")
make_metric(m5, "Vibration", f"{current['vibration']:.2f}")
make_metric(m6, "Fuel Flow", f"{current['fuel_flow']:.0f}", " kg/h")

st.write("")

# ----------------- UI ROW 2: AGENT STATUS -----------------
st.markdown("### 🤖 Agent System Status")
a1, a2, a3, a4, a5 = st.columns(5)

def make_badge(col, label, value):
    col.markdown(f"**{label}**<br><span class='risk-badge risk-{value}'>{value}</span>", unsafe_allow_html=True)

make_badge(a1, "Engine Agent", current['engine_risk'])
make_badge(a2, "Weather Agent", current['weather_risk'])
make_badge(a3, "Stability Agent", current['stability_risk'])
make_badge(a4, "ML Anomaly Agent", current['anomaly_label'])
make_badge(a5, "🔥 OVERALL FUSION RISK", current['overall_risk'])

# ----------------- UI ROW 3: XAI & ADVISORY -----------------
c_xai, c_adv = st.columns(2)

with c_xai:
    st.markdown("#### 🧠 XAI Explanation Agent")
    st.markdown(f'<div class="xai-box">🔍 {current["xai_explanation"]}</div>', unsafe_allow_html=True)

with c_adv:
    st.markdown("#### 📢 Pilot Advisory Agent")
    st.markdown(f'<div class="advisory-box">🔈 {current["advisory_message"]}</div>', unsafe_allow_html=True)

st.write("")
st.divider()

# ----------------- UI ROW 4: CHARTS -----------------
st.markdown("### 📈 Time-Series Analysis")
fig = make_subplots(rows=2, cols=2, 
                    subplot_titles=("Altitude & Speed", "Engine Temp & Vibration", 
                                    "Wind Speed", "Anomaly ML Score"),
                    vertical_spacing=0.15)

# P1: Alt & Speed
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['altitude'], name="Altitude", line=dict(color='#38bdf8', width=2)), row=1, col=1)
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['speed'], name="Speed", yaxis="y2", line=dict(color='#818cf8', width=2)), row=1, col=1)

# P2: Engine
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['engine_temp'], name="Engine Temp", line=dict(color='#f43f5e', width=2)), row=1, col=2)
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['vibration'], name="Vibration", yaxis="y4", line=dict(color='#fbbf24', width=2)), row=1, col=2)

# P3: Weather
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['wind_speed'], name="Wind Speed", fill='tozeroy', fillcolor='rgba(52, 211, 153, 0.1)', line=dict(color='#34d399', width=2)), row=2, col=1)

# P4: Anomaly Score
fig.add_trace(go.Scatter(x=df_view['timestamp'], y=df_view['anomaly_score'], name="ML Anomaly Score", fill='tozeroy', fillcolor='rgba(192, 132, 252, 0.1)', line=dict(color='#c084fc', width=2)), row=2, col=2)

fig.update_layout(
    template="plotly_dark",
    height=600, showlegend=False, 
    margin=dict(l=20, r=20, t=40, b=20), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Outfit, sans-serif")
)
st.plotly_chart(fig, use_container_width=True)

# ----------------- UI ROW 5: ALERT LOG -----------------
st.markdown("### 🚨 Recent Critical Alerts Log")
# Filter to warnings/critical for the table
danger_df = df_view[df_view['overall_risk'].isin(['CRITICAL', 'WARNING'])].tail(10)
if not danger_df.empty:
    st.dataframe(
        danger_df[['timestamp', 'overall_risk', 'engine_risk', 'weather_risk', 'stability_risk', 'anomaly_label', 'advisory_message', 'xai_explanation']],
        use_container_width=True, hide_index=True
    )
else:
    st.success("No abnormal alerts on recent flight timeline.")

# ----------------- UI ROW 6: REPORT EXPORT -----------------
st.divider()
st.markdown("### 📥 Download Structured Reports")
st.markdown("Export the complete telemetry and analysis log for further investigation.")

@st.cache_data
def convert_df(df_in):
    return df_in.to_csv(index=False).encode('utf-8')

csv_data = convert_df(df_view)

st.download_button(
    label="Download Full Flight Report (CSV)",
    data=csv_data,
    file_name="flight_analysis_report.csv",
    mime="text/csv",
    type="primary"
)
