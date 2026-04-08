import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- 🔑 CREDENTIALS ---
API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"

# 🔥 Firebase URL (YOURS)
FIREBASE_URL = "https://iot-enabled-smart-irrigation-default-rtdb.asia-southeast1.firebasedatabase.app"

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

# 🌱 Disease Solutions Dictionary
disease_solutions = {
    "healthy": "✅ Your plant is healthy! Maintain proper watering and sunlight.",
    "bacterial spot": "🦠 Remove infected leaves. Use copper-based fungicide.",
    "early blight": "🍂 Use fungicide sprays. Remove affected leaves.",
    "late blight": "⚠️ Remove infected plants. Apply fungicides.",
    "leaf mold": "🌫 Improve air circulation. Reduce humidity.",
    "septoria leaf spot": "🔬 Remove infected leaves. Apply fungicide.",
    "spider mites": "🕷 Spray neem oil or insecticidal soap.",
    "target spot": "🎯 Use resistant varieties.",
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

                    prediction_lower = prediction.lower()
                    solution = disease_solutions.get(
                        prediction_lower,
                        "⚠️ No solution found."
                    )

                    st.markdown("### 🩺 Recommended Solution")
                    st.write(solution)

                    # 🔥 Send disease status to Firebase
                    requests.put(f"{FIREBASE_URL}/disease.json", json=prediction)

                else:
                    st.error(f"❌ Roboflow Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Processing Error: {e}")

# ---------------- SENSOR DATA ----------------
st.header("📡 Live Sensor Data")

def get_sensor():
    try:
        res = requests.get(f"{FIREBASE_URL}/sensor.json")
        return res.json()
    except:
        return None

if st.button("Get Sensor Data"):
    data = get_sensor()
    if data:
        moisture = data.get("moisture", 0)

        st.success(f"🌱 Moisture: {moisture}")

        if moisture > 3000:
            st.warning("Soil is DRY 🚨")
        elif moisture > 2000:
            st.info("Soil is MEDIUM 🙂")
        else:
            st.success("Soil is WET 💧")
    else:
        st.error("❌ Failed to fetch data")

# ---------------- PUMP CONTROL ----------------
st.header("🚿 Pump Control")

def control_pump(pump, state):
    try:
        requests.put(f"{FIREBASE_URL}/control/{pump}.json", json=state)
        st.success(f"{pump} → {state}")
    except:
        st.error("❌ Failed to send command")

col1, col2 = st.columns(2)

with col1:
    if st.button("Pump1 ON"):
        control_pump("pump1", "ON")
    if st.button("Pump1 OFF"):
        control_pump("pump1", "OFF")

with col2:
    if st.button("Pump2 ON"):
        control_pump("pump2", "ON")
    if st.button("Pump2 OFF"):
        control_pump("pump2", "OFF")
