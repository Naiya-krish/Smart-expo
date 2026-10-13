import random
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. Page Configuration & Custom Dark CSS
# ==========================================
st.set_page_config(
    page_title="Qualcomm Smart Kiosk | Live Edge Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Modern Dark Theme
st.markdown("""
<style>
    /* Main Background & Typography */
    .stApp {
        background-color: #0E1117;
        color: #E0E6ED;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-title {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 25px;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    /* Kiosk Status Cards */
    .status-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .status-idle { background: rgba(100, 116, 139, 0.15); border-left: 5px solid #64748B; }
    .status-viewer { background: rgba(234, 179, 8, 0.15); border-left: 5px solid #EAB308; }
    .status-group { background: rgba(59, 130, 246, 0.15); border-left: 5px solid #3B82F6; }
    .status-active { background: rgba(34, 197, 94, 0.15); border-left: 5px solid #22C55E; }

    /* Footer Banner */
    .privacy-banner {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 10px;
        padding: 12px 20px;
        text-align: center;
        color: #94A3B8;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Database Initialization
# ==========================================
def init_db():
    conn = sqlite3.connect("kiosk_aggregates.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            passers_by INTEGER,
            approachers INTEGER,
            viewers INTEGER,
            engagers INTEGER,
            wifi_density INTEGER
        )
    """)
    conn.commit()
    return conn

conn = init_db()

# ==========================================
# 3. Header & Sidebar Controls
# ==========================================
st.markdown('<p class="main-title">🛍️ Smart Retail Kiosk: Live Engagement Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Qualcomm Arduino UNO Q • Dual-Brain Architecture (Linux MPU + STM32 MCU) • DPDP Act Compliant</p>', unsafe_allow_html=True)

st.sidebar.markdown("### 🎛️ Simulation Engine")
simulate_live = st.sidebar.toggle("Run Live Data Stream", value=True)
crowd_level = st.sidebar.slider("Ambient Foot Traffic Intensity", 5, 100, 25)

st.sidebar.divider()
st.sidebar.markdown("### 📶 Qualcomm 5G Module Status")
sim_5g_active = st.sidebar.toggle("Enable USB 5G Backhaul", value=True)

# ==========================================
# 4. Sensor Simulation & Local Store Logic
# ==========================================
if simulate_live:
    passers = random.randint(crowd_level, crowd_level + 20)
    approachers = int(passers * random.uniform(0.4, 0.7))
    viewers = int(approachers * random.uniform(0.5, 0.8))
    engagers = int(viewers * random.uniform(0.2, 0.4))
    wifi_count = passers + random.randint(-3, 5)
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics (passers_by, approachers, viewers, engagers, wifi_density) VALUES (?, ?, ?, ?, ?)",
        (passers, approachers, viewers, engagers, wifi_count)
    )
    conn.commit()

df = pd.read_sql("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 30", conn)

# ==========================================
# 5. Executive Metric Cards
# ==========================================
if not df.empty:
    m1, m2, m3, m4, m5 = st.columns(5)
    
    current_passers = int(df.iloc[0]["passers_by"])
    current_viewers = int(df.iloc[0]["viewers"])
    current_engagers = int(df.iloc[0]["engagers"])
    
    # Calculate conversion rate for insight
    conversion_rate = round((current_viewers / current_passers * 100), 1) if current_passers > 0 else 0
    
    m1.metric("🚶 Passers-by", current_passers, delta=f"{random.randint(-2, 5)} vs avg")
    m2.metric("👟 Approachers", int(df.iloc[0]["approachers"]))
    m3.metric("👀 Viewers", current_viewers, delta=f"{conversion_rate}% Conv.")
    m4.metric("🗣️ Engagers", current_engagers)
    m5.metric("📶 Wi-Fi Density", int(df.iloc[0]["wifi_density"]))

st.write("")

# ==========================================
# 6. Interactive Visualizations & State Machine
# ==========================================
tab1, tab2 = st.columns([1.2, 1])

with tab1:
    st.markdown("#### 📊 Real-Time Audience Engagement Funnel")
    if not df.empty:
        funnel_data = pd.DataFrame({
            "Funnel Stage": ["1. Passer-by", "2. Approacher", "3. Viewer", "4. Engager"],
            "Visitors": [
                df.iloc[0]["passers_by"],
                df.iloc[0]["approachers"],
                df.iloc[0]["viewers"],
                df.iloc[0]["engagers"]
            ]
        }).set_index("Funnel Stage")
        
        st.bar_chart(funnel_data, height=280)

with tab2:
    st.markdown("#### 🖥️ Adaptive Kiosk Content State")
    if not df.empty:
        curr_v = df.iloc[0]["viewers"]
        curr_e = df.iloc[0]["engagers"]
        
        if curr_e > 2:
            st.markdown("""
                <div class="status-card status-active">
                    <h3 style="color:#22C55E; margin:0;">🗣️ Interactive Voice Mode</h3>
                    <p style="margin:5px 0 0 0; color:#CBD5E1;">Trigger: Voice command / Active engagement detected.<br><b>Action:</b> Displaying dynamic event schedule & maps.</p>
                </div>
            """, unsafe_allow_html=True)
        elif curr_v > 1:
            st.markdown("""
                <div class="status-card status-group">
                    <h3 style="color:#3B82F6; margin:0;">👥 Group Highlight Loop</h3>
                    <p style="margin:5px 0 0 0; color:#CBD5E1;">Trigger: Multiple viewers detected in perimeter.<br><b>Action:</b> Playing multi-user highlight showcase reel.</p>
                </div>
            """, unsafe_allow_html=True)
        elif curr_v == 1:
            st.markdown("""
                <div class="status-card status-viewer">
                    <h3 style="color:#EAB308; margin:0;">🎯 Single Viewer Spotlight</h3>
                    <p style="margin:5px 0 0 0; color:#CBD5E1;">Trigger: 1 viewer facing screen (Dwell > 2s).<br><b>Action:</b> Showing detailed product specifications.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="status-card status-idle">
                    <h3 style="color:#94A3B8; margin:0;">✨ Attract Mode (Idle)</h3>
                    <p style="margin:5px 0 0 0; color:#CBD5E1;">Trigger: No active viewers nearby.<br><b>Action:</b> Displaying ambient high-contrast animation loop.</p>
                </div>
            """, unsafe_allow_html=True)

st.divider()

# ==========================================
# 7. 5G Backhaul Telemetry & Export
# ==========================================
col_telemetry, col_export = st.columns([1, 1])

with col_telemetry:
    st.markdown("#### 📡 Telemetry & Historical Trends")
    if not df.empty:
        st.line_chart(df.set_index("timestamp")[["passers_by", "viewers", "engagers"]].head(15), height=200)

with col_export:
    st.markdown("#### 📁 Data Export & Compliance")
    st.write("Download anonymized session aggregate logs for offline business intelligence and venue heatmap processing.")
    
    if not df.empty:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Session Aggregates (CSV)",
            data=csv_data,
            file_name="kiosk_engagement_aggregates.csv",
            mime="text/csv",
            use_container_width=True
        )

# 5G Sidebar Integration
if sim_5g_active:
    st.sidebar.success("Connected: 5G Standalone (SA)")
    st.sidebar.caption("Protocol: 5G NR (Sub-6GHz) | Latency: 8ms")
    
    if not df.empty:
        payload = {
            "kiosk_id": "expo_kiosk_uno_q_01",
            "backhaul": "Qualcomm_5G_USB_Module",
            "signal_dbm": random.randint(-70, -58),
            "payload": df.head(1).to_dict(orient="records")
        }
        with st.sidebar.expander("🔍 Inspect 5G JSON Payload"):
            st.json(payload)
else:
    st.sidebar.warning("Offline / Local Wi-Fi 5 Fallback")

# ==========================================
# 8. Privacy Guarantee Footer
# ==========================================
st.write("")
st.markdown("""
<div class="privacy-banner">
    🔒 <b>Privacy-by-Design Guarantee:</b> Processing is performed 100% on-device on the Qualcomm Arduino UNO Q. No raw video frames, audio recordings, or Wi-Fi MAC addresses are stored or transmitted. Adheres to India's DPDP Act.
</div>
""", unsafe_allow_html=True)
