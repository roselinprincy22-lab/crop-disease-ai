import streamlit as st
import requests
from PIL import Image
import io

# --- 🔑 CREDENTIALS ---
API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"

# ⚠️ UPDATE THIS WITH YOUR ESP32 IP FROM SERIAL MONITOR
ESP32_IP = "10.145.234.126"   # 🔥 CHANGE THIS

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.title("🌿 SmartAgri Pro")
st.write("👋 Hello, Roselin Princy!")

# 🌱 Disease Solutions
disease_solutions = {
    "healthy": "✅ Plant is healthy.",
    "bacterial spot": "🦠 Use copper fungicide.",
    "early blight": "🍂 Remove infected leaves.",
    "late blight": "⚠️ Use fungicide immediately.",
    "leaf mold": "🌫 Reduce humidity.",
    "septoria leaf spot": "🔬 Apply fungicide.",
    "spider mites": "🕷 Use neem oil spray.",
    "target spot": "🎯 Improve spacing.",
    "yellow leaf curl virus": "🦟 Control whiteflies."
}

# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader("📤 Upload leaf image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("🚀 Diagnose"):
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            buffered.seek(0)

            url = f"https://classify.roboflow.com/{MODEL_ID}"

            response = requests.post(
                url,
                params={"api_key": API_KEY},
                files={"file": buffered},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                prediction = data['predictions'][0]['class']
                confidence = data['predictions'][0]['confidence']

                st.success(f"🌱 Detected: {prediction}")
                st.info(f"Confidence: {confidence:.2%}")

                # Solution match
                prediction_lower = prediction.lower()
                solution = "⚠️ No solution found"

                for key in disease_solutions:
                    if key in prediction_lower:
                        solution = disease_solutions[key]

                st.write("### 🩺 Solution")
                st.write(solution)

                # Auto pump trigger
                if "healthy" not in prediction_lower:
                    try:
                        requests.get(f"{ESP32_IP}/pump1_on", timeout=3)
                        st.warning("🚿 Pump1 Activated")
                    except:
                        st.error("ESP32 not reachable for pump")

            else:
                st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- SENSOR DATA ----------------
st.header("🌡️ Live Sensor Data")

if st.button("📡 Get Sensor Data"):
    try:
        res = requests.get(f"{ESP32_IP}/data", timeout=5)

        if res.status_code == 200:
            data = res.json()

            soil = data.get("soil", 0)
            water = data.get("water", 0)

            st.success(f"🌱 Soil: {soil}")
            st.info(f"💧 Water: {water}")

            if soil > 3000:
                st.warning("🌵 Dry Soil")
            elif soil > 1500:
                st.info("🌿 Medium Soil")
            else:
                st.success("💧 Wet Soil")

        else:
            st.error("ESP32 responded with error")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to ESP32 (check IP & WiFi)")
    except requests.exceptions.Timeout:
        st.error("⏳ ESP32 not responding (timeout)")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- MANUAL CONTROL ----------------
st.header("🛠️ Manual Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚿 Pump1 ON"):
        try:
            requests.get(f"{ESP32_IP}/pump1_on", timeout=3)
            st.success("Pump1 ON")
        except:
            st.error("ESP32 not connected")

    if st.button("🛑 Pump1 OFF"):
        try:
            requests.get(f"{ESP32_IP}/pump1_off", timeout=3)
        except:
            st.error("ESP32 error")

with col2:
    if st.button("🚿 Pump2 ON"):
        try:
            requests.get(f"{ESP32_IP}/pump2_on", timeout=3)
            st.success("Pump2 ON")
        except:
            st.error("ESP32 not connected")

    if st.button("🛑 Pump2 OFF"):
        try:
            requests.get(f"{ESP32_IP}/pump2_off", timeout=3)
        except:
            st.error("ESP32 error")
