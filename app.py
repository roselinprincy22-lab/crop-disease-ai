import streamlit as st
import requests
from PIL import Image
import io

# --- 🔑 CREDENTIALS ---
API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"
# ⚠️ MAKE SURE THIS MATCHES WHAT THE SERIAL MONITOR PRINTS
ESP32_IP = "http://10.145.234.126" 

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")
st.title("🌿 SmartAgri Pro")
st.write("👋 Hello, Roselin Princy!")

disease_solutions = {
    "healthy": "✅ Plant is healthy. Keep up the good work!",
    "bacterial spot": "🦠 Use copper fungicide.",
    "early blight": "🍂 Remove infected leaves.",
    "late blight": "⚠️ Use fungicide immediately.",
    "leaf mold": "🌫 Reduce humidity.",
    "septoria leaf spot": "🔬 Apply fungicide.",
    "spider mites": "🕷 Use neem oil spray.",
    "target spot": "🎯 Improve spacing.",
    "yellow leaf curl virus": "🦟 Control whiteflies."
}

# ---------------- IMAGE UPLOAD & DIAGNOSIS ----------------
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
            response = requests.post(url, params={"api_key": API_KEY}, files={"file": buffered}, timeout=10)

            if response.status_code == 200:
                data = response.json()
                prediction = data['predictions'][0]['class']
                confidence = data['predictions'][0]['confidence']

                st.success(f"🌱 Detected: {prediction}")
                st.info(f"Confidence: {confidence:.2%}")

                prediction_lower = prediction.lower()
                solution = "⚠️ No solution found"

                # --- BALLOONS & SOLUTION LOGIC ---
                if "healthy" in prediction_lower:
                    st.balloons()  # 🎈 Celebrate!
                    solution = disease_solutions["healthy"]
                else:
                    for key in disease_solutions:
                        if key in prediction_lower:
                            solution = disease_solutions[key]
                    
                    # Auto pump trigger for sick plants
                    try:
                        requests.get(f"{ESP32_IP}/pump1_on", timeout=2)
                        st.warning("🚿 Disease detected: Pump1 Activated for treatment.")
                    except:
                        st.error("📡 ESP32 unreachable for auto-pump.")

                st.write("### 🩺 Solution")
                st.write(solution)
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- SENSOR DATA & MANUAL CONTROL ----------------
st.divider()
st.header("🌡️ Live Sensor Data")

if st.button("📡 Get Sensor Data"):
    try:
        res = requests.get(f"{ESP32_IP}/data", timeout=3)
        if res.status_code == 200:
            sensor_data = res.json()
            soil = sensor_data.get("soil", 0)
            st.metric("Soil Moisture", soil)
            if soil > 3000: st.warning("🌵 Dry Soil")
            else: st.success("💧 Soil is Good")
    except:
        st.error("❌ Connection Failed. Is the ESP32 on the same WiFi?")

st.header("🛠️ Manual Control")
col1, col2 = st.columns(2)
with col1:
    if st.button("🚿 Pump1 ON"):
        requests.get(f"{ESP32_IP}/pump1_on", timeout=2)
    if st.button("🛑 Pump1 OFF"):
        requests.get(f"{ESP32_IP}/pump1_off", timeout=2)
