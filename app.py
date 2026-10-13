import random
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# Smart Retail / Expo Kiosk — polished dark/light dashboard
# ------------------------------------------------------------
st.set_page_config(
    page_title="Smart Kiosk | Engagement Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = "kiosk_aggregates.db"


@st.cache_resource
def init_db():
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            passers_by INTEGER,
            approachers INTEGER,
            viewers INTEGER,
            engagers INTEGER,
            wifi_density INTEGER
        )
        """
    )
    connection.commit()
    return connection


conn = init_db()


def inject_theme(theme_name: str):
    """Apply app-level colors; Streamlit's own menus may follow its base theme."""
    dark = theme_name == "Dark"
    if dark:
        colors = {
            "bg": "#071326",
            "panel": "#081320",
            "panel2": "#0660AA",
            "text": "#1AF7FF",
            "muted": "#9db2d0",
            "border": "rgba(51, 153, 255, 0.32)",
            "accent": "#05daff",
            "accent2": "#7c5cff",
            "sidebar": "#08152a",
            "shadow": "0 12px 32px rgba(0, 0, 0, 0.20)",
        }
    else:
        colors = {
            "bg": "#009494AB",
            "panel": "#e2ffbc",
            "panel2": "#e0fd3a",
            "text": "#17263e",
            "muted": "#61718a",
            "border": "rgba(49, 105, 180, 0.18)",
            "accent": "#087fce",
            "accent2": "#7355d9",
            "sidebar": "#E2FF7A",
            "shadow": "0 10px 28px rgba(30, 64, 110, 0.08)",
        }

    st.markdown(
        f"""
        <style>
        :root {{
          --app-bg: {colors['bg']};
          --panel: {colors['panel']};
          --panel2: {colors['panel2']};
          --app-text: {colors['text']};
          --muted: {colors['muted']};
          --border: {colors['border']};
          --accent: {colors['accent']};
          --accent2: {colors['accent2']};
          --sidebar: {colors['sidebar']};
          --shadow: {colors['shadow']};
        }}

        .stApp {{
          background:
            radial-gradient(ellipse at 12% 0%, rgba(25, 211, 243, 0.08), transparent 32%),
            radial-gradient(ellipse at 95% 8%, rgba(124, 92, 255, 0.08), transparent 28%),
            var(--app-bg);
          color: var(--app-text);
        }}
        [data-testid="stHeader"] {{
          background: transparent;
        }}
        [data-testid="stSidebar"] {{
          background: var(--sidebar);
          border-right: 1px solid var(--border);
        }}
        [data-testid="stSidebar"] * {{
          color: var(--app-text);
        }}
        .block-container {{
          padding-top: 1.35rem;
          padding-bottom: 2rem;
          max-width: 1600px;
        }}
        h1, h2, h3, h4, p, label, [data-testid="stMetricLabel"] {{
          color: var(--app-text);
        }}
        .hero {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 1rem;
          padding: 1.25rem 1.4rem;
          border: 1px solid var(--border);
          border-radius: 20px;
          background: linear-gradient(120deg, var(--panel), var(--panel2));
          box-shadow: var(--shadow);
          margin-bottom: 1.15rem;
        }}
        .eyebrow {{
          color: var(--accent);
          text-transform: uppercase;
          letter-spacing: .14em;
          font-size: .72rem;
          font-weight: 800;
          margin-bottom: .35rem;
        }}
        .hero-title {{
          font-size: clamp(1.6rem, 2.8vw, 2.45rem);
          font-weight: 850;
          letter-spacing: -.04em;
          line-height: 1.12;
          margin: 0;
          color: var(--app-text);
        }}
        .hero-subtitle {{
          color: var(--muted);
          margin-top: .5rem;
          font-size: .95rem;
        }}
        .live-pill {{
          display: inline-flex;
          align-items: center;
          gap: .45rem;
          white-space: nowrap;
          padding: .48rem .8rem;
          border: 1px solid rgba(0, 205, 160, .35);
          border-radius: 999px;
          color: #00b98a;
          background: rgba(0, 185, 138, .09);
          font-size: .8rem;
          font-weight: 800;
        }}
        .live-dot {{
          height: .5rem; width: .5rem; border-radius: 50%;
          background: #00d6a0; display: inline-block;
          box-shadow: 0 0 12px rgba(0, 214, 160, .7);
        }}
        .metric-card {{
          border: 1px solid var(--border);
          background: var(--panel);
          box-shadow: var(--shadow);
          border-radius: 17px;
          padding: 1rem 1rem .85rem;
          min-height: 145px;
          transition: transform .18s ease, border-color .18s ease;
        }}
        .metric-card:hover {{
          transform: translateY(-3px);
          border-color: var(--accent);
        }}
        .metric-top {{
          display: flex; align-items: center; gap: .65rem;
          color: var(--muted); font-size: .83rem; font-weight: 650;
        }}
        .metric-icon {{
          width: 2.25rem; height: 2.25rem; display: grid;
          place-items: center; border-radius: 12px;
          background: rgba(25, 211, 243, .12); font-size: 1.15rem;
        }}
        .metric-value {{
          font-size: 2rem; font-weight: 850; letter-spacing: -.04em;
          margin-top: .45rem; color: var(--app-text);
        }}
        .metric-note {{
          font-size: .76rem; color: var(--muted); margin-top: .1rem;
        }}
        .section-card {{
          border: 1px solid var(--border);
          border-radius: 18px;
          padding: 1.05rem 1.15rem;
          background: var(--panel);
          box-shadow: var(--shadow);
          min-height: 100%;
        }}
        .section-heading {{
          display: flex; align-items: center; gap: .6rem;
          font-weight: 800; font-size: 1.05rem;
          margin-bottom: .85rem; color: var(--app-text);
        }}
        .state-box {{
          border-radius: 15px;
          padding: 1rem;
          background: var(--panel2);
          border: 1px solid var(--border);
          margin-top: .65rem;
        }}
        .state-label {{
          color: var(--muted); text-transform: uppercase;
          font-size: .72rem; letter-spacing: .1em; font-weight: 800;
        }}
        .state-value {{
          font-size: 1.05rem; font-weight: 800;
          margin-top: .35rem; color: var(--accent);
        }}
        .small-muted {{ color: var(--muted); font-size: .82rem; }}
        .status-row {{
          display: flex; justify-content: space-between; gap: .8rem;
          padding: .55rem 0; border-bottom: 1px solid var(--border);
          font-size: .84rem;
        }}
        .status-row:last-child {{ border-bottom: 0; }}
        .privacy-footer {{
          margin-top: 1.2rem; padding: .9rem 1.1rem;
          border: 1px solid var(--border); border-radius: 14px;
          background: var(--panel2); color: var(--muted);
          font-size: .82rem;
        }}
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stButton"] button {{
          border-radius: 10px; border: 1px solid var(--border);
          font-weight: 700;
        }}
        div[data-testid="stMetric"] {{
          background: var(--panel);
          padding: .7rem .85rem;
          border-radius: 12px;
          border: 1px solid var(--border);
        }}
        hr {{ border-color: var(--border); }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Sidebar
with st.sidebar:
    st.markdown("## 🖥️ SMART **KIOSK**")
    st.caption("REAL-TIME ENGAGEMENT ANALYTICS")
    st.divider()

    st.markdown("### 🎨 Appearance")
    theme = st.radio(
        "Choose dashboard theme",
        ["Dark", "Light"],
        horizontal=True,
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 🎛️ Simulation Controls")
    simulate_live = st.toggle("Run Live Data Simulation", value=True)
    crowd_level = st.slider("Ambient Foot Traffic Level", 1, 50, 15)

    st.divider()
    st.markdown("### 📶 Qualcomm 5G Module")
    sim_5g_active = st.toggle("Enable simulated 5G backhaul", value=True)

inject_theme(theme)

# Add one aggregate sample per rerun while simulation is enabled.
if simulate_live:
    passers = random.randint(crowd_level, crowd_level + 20)
    approachers = int(passers * random.uniform(0.4, 0.7))
    viewers = int(approachers * random.uniform(0.5, 0.8))
    engagers = int(viewers * random.uniform(0.2, 0.4))
    wifi_count = max(0, passers + random.randint(-3, 5))

    conn.execute(
        """
        INSERT INTO metrics
        (passers_by, approachers, viewers, engagers, wifi_density)
        VALUES (?, ?, ?, ?, ?)
        """,
        (passers, approachers, viewers, engagers, wifi_count),
    )
    conn.commit()

df = pd.read_sql_query(
    "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 100",
    conn,
)
latest = df.iloc[0] if not df.empty else None

# Header
header_left, header_right = st.columns([5, 1.35])
with header_left:
    st.markdown(
        """
        <div class="hero">
          <div>
            <div class="eyebrow">Edge AI · Sensor Fusion · Live Engagement</div>
            <div class="hero-title">🛍️ Smart Retail Analytics</div>
            <div class="hero-subtitle">A real-time overview of kiosk traffic and audience engagement</div>
          </div>
          <div class="live-pill"><span class="live-dot"></span> SIMULATION</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_right:
    st.markdown(
        f"""
        <div class="section-card" style="text-align:center; padding:1rem .5rem;">
          <div class="small-muted">DASHBOARD THEME</div>
          <div style="font-size:1.15rem;font-weight:800;margin:.35rem 0;">{"🌙 Dark" if theme == "Dark" else "☀️ Light"}</div>
          <div class="small-muted">{datetime.now().strftime("%d %b %Y · %H:%M:%S")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# KPI cards
st.markdown("### Live Engagement Snapshot")
if latest is not None:
    kpis = [
        ("🚶", "Passers-by", int(latest["passers_by"]), "People passing the kiosk"),
        ("👟", "Approachers", int(latest["approachers"]), "Stopped or moved closer"),
        ("👀", "Viewers", int(latest["viewers"]), "Viewed kiosk content"),
        ("💬", "Engagers", int(latest["engagers"]), "Interacted with the kiosk"),
        ("📶", "Wi-Fi Density", int(latest["wifi_density"]), "Simulated cross-check"),
    ]
    cols = st.columns(5)
    for col, (icon, label, value, note) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                  <div class="metric-top"><span class="metric-icon">{icon}</span>{label}</div>
                  <div class="metric-value">{value:,}</div>
                  <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("No metrics yet. Enable the simulation to generate sample data.")

st.write("")

# Conversion calculations
if latest is not None:
    passers_n = max(int(latest["passers_by"]), 0)
    approachers_n = max(int(latest["approachers"]), 0)
    viewers_n = max(int(latest["viewers"]), 0)
    engagers_n = max(int(latest["engagers"]), 0)

    def pct(numerator, denominator):
        return (numerator / denominator * 100) if denominator else 0

    c1, c2 = st.columns([1.15, 0.85], gap="large")

    with c1:
        st.markdown(
            '<div class="section-card"><div class="section-heading">📊 Engagement Funnel</div>',
            unsafe_allow_html=True,
        )
        funnel = pd.DataFrame(
            {
                "Stage": ["Passers-by", "Approachers", "Viewers", "Engagers"],
                "Count": [passers_n, approachers_n, viewers_n, engagers_n],
            }
        ).set_index("Stage")
        st.bar_chart(funnel, color="#19bff3", height=260)
        st.markdown(
            f"""
            <div class="status-row"><span>Passer-by → Approacher</span><strong>{pct(approachers_n, passers_n):.1f}%</strong></div>
            <div class="status-row"><span>Approacher → Viewer</span><strong>{pct(viewers_n, approachers_n):.1f}%</strong></div>
            <div class="status-row"><span>Viewer → Engager</span><strong>{pct(engagers_n, viewers_n):.1f}%</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            '<div class="section-card"><div class="section-heading">🖥️ Adaptive Kiosk Content</div>',
            unsafe_allow_html=True,
        )
        if engagers_n > 2:
            state_icon = "🎙️"
            state = "Interactive experience"
            detail = "Voice command / interactive schedule display is selected."
        elif viewers_n > 1:
            state_icon = "🎬"
            state = "Group highlight video"
            detail = "A group-focused highlight video loop is selected."
        elif viewers_n == 1:
            state_icon = "🔎"
            state = "Product details"
            detail = "Detailed product specifications are selected for one viewer."
        else:
            state_icon = "✨"
            state = "Attract mode"
            detail = "Idle animation is selected while no viewers are detected."

        st.markdown(
            f"""
            <div class="state-box">
              <div style="font-size:2.4rem">{state_icon}</div>
              <div class="state-label">Current content state</div>
              <div class="state-value">{state}</div>
              <p class="small-muted">{detail}</p>
            </div>
            <div style="margin-top:1rem">
              <div class="status-row"><span>Viewer engagement</span><strong>{pct(engagers_n, viewers_n):.1f}%</strong></div>
              <div class="status-row"><span>Estimated audience reach</span><strong>{viewers_n:,}</strong></div>
              <div class="status-row"><span>Content mode</span><strong>Adaptive (simulated)</strong></div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown(
            '<div class="section-card"><div class="section-heading">📈 Recent Engagement History</div>',
            unsafe_allow_html=True,
        )
        history = df.copy()
        history["timestamp"] = pd.to_datetime(history["timestamp"], errors="coerce")
        history = history.dropna(subset=["timestamp"]).sort_values("timestamp")
        if not history.empty:
            history = history.set_index("timestamp")
            st.line_chart(
                history[["passers_by", "approachers", "viewers", "engagers"]],
                color=["#19bff3", "#377dff", "#8b5cf6", "#f04db8"],
                height=260,
            )
        else:
            st.caption("History will appear after samples are recorded.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="section-card"><div class="section-heading">📡 5G Backhaul Status</div>',
            unsafe_allow_html=True,
        )
        if sim_5g_active:
            signal = random.randint(-72, -55)
            quality = "Excellent" if signal >= -65 else "Good"
            st.success("Connected · Simulated 5G Standalone (SA)")
            st.markdown(
                f"""
                <div class="status-row"><span>Signal strength</span><strong>{signal} dBm · {quality}</strong></div>
                <div class="status-row"><span>Network</span><strong>5G NR (Sub-6GHz)</strong></div>
                <div class="status-row"><span>Backhaul mode</span><strong>Aggregates only</strong></div>
                <div class="status-row"><span>Transport</span><strong>Simulated</strong></div>
                """,
                unsafe_allow_html=True,
            )
            payload = {
                "kiosk_id": "expo_kiosk_01",
                "network": "5G NR (Sub-6GHz) — simulated",
                "signal_strength_dbm": signal,
                "data_packet": {
                    "timestamp": str(latest["timestamp"]),
                    "passers_by": passers_n,
                    "approachers": approachers_n,
                    "viewers": viewers_n,
                    "engagers": engagers_n,
                    "wifi_density": int(latest["wifi_density"]),
                },
            }
            with st.expander("🔍 Inspect simulated JSON payload"):
                st.json(payload)
        else:
            st.warning("Backhaul disabled · local-only simulation")
            st.caption("Metrics remain in the local SQLite database.")
        st.markdown("</div>", unsafe_allow_html=True)

# Export section
st.write("")
st.markdown("### 📁 Session Reports")
if not df.empty:
    export_df = df.copy()
    csv_data = export_df.to_csv(index=False).encode("utf-8")
    e1, e2 = st.columns([1, 3])
    with e1:
        st.download_button(
            "⬇️ Download CSV report",
            data=csv_data,
            file_name="kiosk_engagement_aggregates.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with e2:
        st.caption(f"{len(df)} most recent aggregate records are included in this export.")

with st.expander("🧾 View recent aggregate records"):
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption("No records available yet.")

st.markdown(
    """
    <div class="privacy-footer">
      🔒 <strong>Privacy by design:</strong> this simulation stores aggregate counts only.
      It does not capture or store raw video, audio recordings, or device MAC addresses.
      Actual sensor and network deployments must be configured and verified separately.
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Smart Kiosk Analytics · Edge AI + Sensor Fusion concept demo")
