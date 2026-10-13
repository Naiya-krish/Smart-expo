*Run it in the terminal r installing the requirement* 
# pip install -r requirements.txt 
*Run it r checking the r viewing the streamlit live simulation*
# streamlit run app.py

*Markdown*
# 🛍️ Smart Retail & Expo Kiosk with Privacy-Preserving Engagement Analytics
**IIITB COMET Foundation × Qualcomm Hackathon 2026 | Track: IoT Applications**

---

## 📌 1. Project Overview & Problem Statement

### **The Problem**
Traditional retail stores and exhibition booths face a major data blind spot. While online platforms track every click, scroll, and dwell time, physical storefronts and expo kiosks rely on crude, primitive solutions—such as basic infrared door counters or manual clickers—which fail to measure real, qualitative visitor engagement. 

Furthermore, existing digital signage solutions are either:
1. **Dumb & Static:** Looping identical video content regardless of who is standing in front of the kiosk.
2. **Privacy-Intrusive & Cost-Prohibitive:** Utilizing heavy cloud-dependent CCTV pipelines that record raw video, risk facial recognition privacy violations (breaching local data protection frameworks like India’s DPDP Act), and require expensive industrial PCs (IPCs) and dedicated GPUs.

### **The Impact**
Retailers and expo organizers need a **low-cost, edge-native, privacy-first analytics and adaptive content engine** that measures true visitor behavior on the fly without violating user privacy.

---

## 💡 2. The Solution & Engagement Funnel

Our project delivers an intelligent, low-cost edge kiosk powered by the Qualcomm-driven **Arduino UNO Q**. Instead of recording or transmitting raw video streams, the system performs local computer vision and sensor fusion at the edge, reducing data streams into an anonymized **4-Stage Engagement Funnel**:

[ 🚶 Passer-by ] ──> [ 👟 Approacher ] ──> [ 👀 Viewer ] ──> [ 🗣️ Engager ]
(Zone Detection)     (Proximity Trigger)    (Attention Lock)    (Voice/Interaction) 

* **Stage 1: Passer-by:** Detected via wide-angle vision tracking or ambient Wi-Fi density probes.
* **Stage 2: Approacher:** Individuals moving closer to the kiosk boundary (monitored by ultra-low-power MCU sensors).
* **Stage 3: Viewer:** Visitors whose head pose / gaze is oriented toward the display screen, triggering dynamic content changes.
* **Stage 4: Engager:** Visitors actively interacting via voice command keywords or touchscreen menus.

---

## 💰 3. Value Proposition & Cost Efficiency

* **Ultra-Low Capital Expenditure (CapEx):** Replaces expensive industrial PCs (which cost $800–$1,500+) with a single compact, low-power single-board computer priced under $60.
* **Zero Cloud Dependency & Bandwidth Savings:** Processing runs entirely locally at the edge. Only lightweight aggregate text records are transmitted over network layers.
* **Privacy-by-Design:** Compliant with modern privacy standards by dropping raw video frames instantly and storing/logging only aggregate telemetry counts.

---

## ⚙️ 4. Hardware Architecture: Why Arduino UNO Q?

This project is built natively around the **Arduino UNO Q**, leveraging its unique **Dual-Brain Architecture**.

### **Detailed Technical Specifications of Arduino UNO Q**
* **Microprocessor (MPU):** Qualcomm Dragonwing™ QRB2210 (Quad-core Arm® Cortex®-A53 @ 2.0 GHz) with integrated Adreno GPU and Dual ISP. Runs **Linux Debian OS**.
* **Microcontroller (MCU):** STMicroelectronics STM32U585 (Arm® Cortex®-M33 @ up to 160 MHz, 2 MB Flash, 786 KB SRAM) running Zephyr RTOS.
* **Memory & Storage:** 2 GB / 4 GB LPDDR4 RAM and 16 GB / 32 GB built-in eMMC storage (no SD card bottleneck).
* **Connectivity:** Dual-band Wi-Fi® 5 (2.4/5 GHz) and Bluetooth® 5.1.
* **Form Factor & Expansion:** Classic UNO shield compatibility paired with a high-speed peripheral header, USB-C (power, display, camera, audio), and Qwiic connector for plug-and-play Modulino nodes.

### **Why Arduino UNO Q Over Other Hardware? (Hardware Replacement Analysis)**

| Traditional / Alternative Setup | Disadvantages | Why Arduino UNO Q Replaces It |
| :--- | :--- | :--- |
| **Separate Raspberry Pi 5 + Arduino Uno** | Requires two separate physical boards, custom serial bridging wiring, messy USB hubs, and bulky enclosures. | **Integrated Dual-Brain:** Combines the Linux-capable Qualcomm MPU and real-time STM32 MCU on a single, compact classic form-factor board. |
| **Industrial PCs (IPCs) / Mini-PCs** | High cost ($500+), high power consumption (requires active cooling/fans), oversized for expo booth deployment. | **Fanless Low-Power Envelope:** Runs efficiently within a tight thermal envelope while offering hardware-accelerated edge AI via Qualcomm's architecture. |
| **Standard Microcontrollers (ESP32 / Arduino R4)** | Lack the processing power for running computer vision models (YOLO/MobileNet) or full Linux Debian applications. | **MPU + MCU Synergy:** Offloads heavy AI vision and web dashboards to the Qualcomm MPU while leaving real-time sensor polling to the STM32 MCU. |

---

## 💻 5. Software Stack & Legacy Replacement

| Component | Traditional Legacy Software | Our Modern Edge Stack | Why We Chose It |
| :--- | :--- | :--- | :--- |
| **Operating System** | Custom embedded Linux distros requiring complex cross-compilation. | **Debian Linux OS** (on MPU) + **Zephyr RTOS** (on MCU) | Upstream-first support, full Docker containerization readiness, and massive package library availability. |
| **Vision & AI Pipeline** | Heavy cloud streaming (RTSP to cloud servers) for processing. | **OpenCV & INT8 Quantized Models** running locally on Qualcomm MPU | Eliminates cloud latency, reduces bandwidth costs to zero, and ensures privacy compliance. |
| **Data Storage** | Remote cloud databases vulnerable to connection drops. | **Local SQLite Embedded Database** | Provides robust, zero-configuration local transaction storage for aggregate metrics even during intermittent network drops. |
| **Development IDE** | Fragmented toolchains across separate IDEs. | **Arduino App Lab** | A unified environment combining C++ Arduino sketches for real-time control with Python scripts for MPU-side AI and networking. |

---

## 🌐 6. Live Online Simulation & Demo

Since physical hardware prototyping can be simulated during early development phases, we have built a fully functional containerized simulation of the backend data pipeline and engagement dashboard.

👉 **[Access the Live Interactive Kiosk Dashboard Simulation Here](https://your-streamlit-app-url.streamlit.app)** *(Replace with your actual Streamlit link)*

### **Simulation Features:**
* Live 4-stage funnel conversion charts (*Passer-by $\rightarrow$ Approacher $\rightarrow$ Viewer $\rightarrow$ Engager*).
* Adaptive kiosk content state triggers based on active crowd density.
* Simulated Qualcomm 5G module telemetry backhaul packet inspector.
* CSV data export for aggregate session logs.

---

## 🚀 7. Getting Started Locally

To run the simulation dashboard locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Naiya-krish/Smart-expo.git](https://github.com/Naiya-krish/Smart-expo.git)
   cd smart-expo-kiosk

   👥 Authors & Acknowledgments:
Developed for the IIITB COMET Foundation × Qualcomm Hackathon 2026.
Powered by Qualcomm Dragonwing™ and Arduino hardware technologies.
