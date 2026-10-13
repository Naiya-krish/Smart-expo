import random
import sqlite3
import pandas as pd
import streamlit as st

# 1. Initialize Local SQLite Aggregate Store (Privacy-Preserving: Counts Only)
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

# Page Configuration
st.set_page_config(page_title="Smart Kiosk Simulation Dashboard", layout="wide")
st.title("🛍️ Smart Retail / Expo Kiosk: Live Engagement Analytics")
st.markdown("*Qualcomm Arduino UNO Q Edge AI & Sensor Fusion Simulation Platform*[cite: 5, 11]")

# Sidebar Controls for Simulation & 5G Backhaul
st.sidebar.header("🎛️ Simulation Controls")
simulate_live = st.sidebar.toggle("Run Live Data Simulation", value=True)
crowd_level = st.sidebar.slider("Ambient Foot Traffic Level", 1, 50, 15)

st.sidebar.divider()
st.sidebar.subheader("📶 Qualcomm 5G Module Status")
sim_5g_active = st.sidebar.toggle("Enable USB 5G Backhaul", value=True)

# 2. Simulate Sensor Inputs & Engagement Funnel Logic[cite: 5, 10]
if simulate_live:
    passers = random.randint(crowd_level, crowd_level + 20)
    approachers = int(passers * random.uniform(0.4, 0.7))
    viewers = int(approachers * random.uniform(0.5, 0.8))
    engagers = int(viewers * random.uniform(0.2, 0.4))
    wifi_count = passers + random.randint(-3, 5)  # Wi-Fi cross-check signal[cite: 6, 21]
    
    # Log aggregate counts only (Privacy by design)[cite: 2, 14]
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics (passers_by, approachers, viewers, engagers, wifi_density) VALUES (?, ?, ?, ?, ?)",
        (passers, approachers, viewers, engagers, wifi_count)
    )
    conn.commit()

# 3. Fetch Data for Dashboard Display[cite: 2, 14]
df = pd.read_sql("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 20", conn)

# Top KPI Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)
if not df.empty:
    col1.metric("🚶 Passers-by", int(df.iloc[0]["passers_by"]))
    col2.metric("👟 Approachers", int(df.iloc[0]["approachers"]))
    col3.metric("👀 Viewers", int(df.iloc[0]["viewers"]))
    col4.metric("🗣️ Engagers", int(df.iloc[0]["engagers"]))
    col5.metric("📶 Wi-Fi Density", int(df.iloc[0]["wifi_density"]))

st.divider()

# Layout: Funnel Chart & Live Content State
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Engagement Funnel Conversion")
    if not df.empty:
        funnel_data = pd.DataFrame({
            "Stage": ["Passer-by", "Approacher", "Viewer", "Engager"],
            "Count": [
                df.iloc[0]["passers_by"],
                df.iloc[0]["approachers"],
                df.iloc[0]["viewers"],
                df.iloc[0]["engagers"]
            ]
        })
        st.bar_chart(funnel_data.set_index("Stage"))

with c2:
    st.subheader("🖥️ Adaptive Kiosk Content State")
    if not df.empty:
        current_viewers = df.iloc[0]["viewers"]
        current_engagers = df.iloc[0]["engagers"]
        
        if current_engagers > 2:
            st.success("State: **Voice Command / Interactive Schedule Display Active**")
        elif current_viewers > 1:
            st.info("State: **Group Highlight Video Loop Playing**")
        elif current_viewers == 1:
            st.warning("State: **Single Viewer Detailed Product Specs Displayed**")
        else:
            st.text("State: **Attract Mode Animation (Idle)**[cite: 3, 27]")

# 4. 5G Backhaul Sidebar Panel
if sim_5g_active:
    st.sidebar.success("Connected: 5G Standalone (SA)")
    st.sidebar.text("Signal: -62 dBm (Excellent)")
    st.sidebar.text("Backhaul Mode: Aggregates Only[cite: 17, 18]")
    
    if not df.empty:
        payload = {
            "kiosk_id": "expo_kiosk_01",
            "network": "5G NR (Sub-6GHz)",
            "signal_strength_dbm": random.randint(-72, -55),
            "data_packet": df.head(1).to_dict(orient="records")
        }
        with st.sidebar.expander("Inspect 5G JSON Payload"):
            st.json(payload)
else:
    st.sidebar.warning("Offline / Local Wi-Fi 5 Fallback")

# CSV Data Export for Organizers
st.divider()
st.subheader("📁 Session Data Export")
if not df.empty:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Aggregate Metrics (CSV)",
        data=csv_data,
        file_name="kiosk_engagement_aggregates.csv",
        mime="text/csv"
    )

# Privacy Guarantee Callout[cite: 14]
st.divider()
st.caption("🔒 **Privacy Guarantee:** Running local SQLite aggregate logging. No raw video frames, audio recordings, or MAC addresses are stored or transmitted[cite: 2, 14].")
