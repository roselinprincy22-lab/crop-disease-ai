import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- 🔑 CREDENTIALS ---
API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"
ESP32_IP = "http://10.145.234.126"

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

# 🌱 Disease Solutions
disease_solutions = {
    "healthy": "✅ Your plant is healthy! Maintain proper watering and sunlight.",
    "bacterial spot": "🦠 Remove infected leaves. Use copper-based fungicide.",
    "early blight": "🍂 Apply fungicide. Remove affected leaves.",
    "late blight": "⚠️ Remove infected plants. Avoid moisture.",
    "leaf mold": "🌫 Improve air circulation. Reduce humidity.",
    "septoria leaf spot": "🔬 Remove infected leaves. Apply fungicide.",
    "spider mites": "🕷 Use neem oil spray.",
    "target spot": "🎯 Use resistant varieties. Apply fungicide.",
    "yellow leaf curl virus": "🦟 Control whiteflies. Remove infected plants."
}

# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader("📤 Upload leaf photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🌿 Current Scan", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("🤖 AI is analyzing leaf health..."):
            
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"

            try:
                response = requests.post(
                    url,
                    data=img_str,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                if response.status_code == 200:
                    data = response.json()

                    prediction = data['predictions'][0]['class']
                    confidence = data['predictions'][0]['confidence']

                    st.success(f"🌱 Detected: {prediction}")
                    st.info(f"📊 Confidence: {confidence:.1%}")

                    # 🔥 SMART MATCH
                    prediction_lower = prediction.lower().strip()
                    solution = None

                    for disease in disease_solutions:
                        if disease in prediction_lower:
                            solution = disease_solutions[disease]
                            break

                    if not solution:
                        solution = "⚠️ No solution found."

                    st.markdown("### 🩺 Recommended Solution")
                    st.write(solution)

                    # 🚨 Auto spray (Pump1 - battery)
                    if "healthy" not in prediction_lower:
                        st.warning("🚨 Disease detected! Spraying...")
                        try:
                            requests.get(f"{ESP32_IP}/pump1_on", timeout=2)
                        except:
                            st.error("ESP32 not connected")
                    else:
                        st.balloons()

                else:
                    st.error(f"❌ Roboflow Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------- SENSOR DATA ----------------
st.markdown("## 🌡️ Live Sensor Data")

if st.button("📡 Get Sensor Data"):
    try:
        res = requests.get(f"{ESP32_IP}/data", timeout=2)
        data = res.json()

        soil = data["soil"]
        water = data["water"]

        st.success(f"🌱 Soil Moisture: {soil}")
        st.info(f"💧 Water Level: {water}")

        # 🌱 Soil condition
        if soil > 3000:
            st.warning("🌵 Soil is DRY")
        elif soil > 1500:
            st.info("🌿 Soil is MEDIUM")
        else:
            st.success("💧 Soil is WET")

    except:
        st.error("❌ ESP32 not connected")

# ---------------- MANUAL CONTROL ----------------
with st.expander("🛠️ Manual Control"):

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚿 Pump1 ON (Battery)"):
            try:
                requests.get(f"{ESP32_IP}/pump1_on")
                st.success("Pump1 ON")
            except:
                st.error("ESP32 not connected")

        if st.button("🛑 Pump1 OFF"):
            try:
                requests.get(f"{ESP32_IP}/pump1_off")
            except:
                st.error("ESP32 error")

    with col2:
        if st.button("🚿 Pump2 ON (Adapter)"):
            try:
                requests.get(f"{ESP32_IP}/pump2_on")
                st.success("Pump2 ON")
            except:
                st.error("ESP32 not connected")

        if st.button("🛑 Pump2 OFF"):
            try:
                requests.get(f"{ESP32_IP}/pump2_off")
            except:
                st.error("ESP32 error")
