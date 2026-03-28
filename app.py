import streamlit as st
import requests
from PIL import Image
import io

# 🔴 CHANGE THIS IP (from Serial Monitor)
ESP32_IP = "http://10.145.234.126"

API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")
st.title("🌿 SmartAgri Pro")

# ---------------- IMAGE DIAGNOSIS ----------------
st.header("📷 Crop Disease Detection")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("Diagnose"):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)

        url = f"https://classify.roboflow.com/{MODEL_ID}"
        response = requests.post(url, params={"api_key": API_KEY}, files={"file": buffered})

        if response.status_code == 200:
            data = response.json()
            pred = data['predictions'][0]['class']

            st.success(f"Detected: {pred}")

            # Auto trigger pump if disease
            if "healthy" not in pred.lower():
                try:
                    requests.get(f"{ESP32_IP}/pump1_on", timeout=5)
                    st.warning("Pump1 Activated")
                except:
                    st.error("ESP32 not reachable")

# ---------------- SENSOR ----------------
st.header("🌡️ Sensor Data")

if st.button("Get Data"):
    try:
        res = requests.get(f"{ESP32_IP}/data", timeout=5)
        data = res.json()
        soil = data["soil"]

        st.metric("Soil Moisture", soil)

        if soil > 3000:
            st.warning("Dry Soil")
        else:
            st.success("Soil Good")

    except:
        st.error("ESP32 not connected")

# ---------------- MANUAL CONTROL ----------------
st.header("🛠️ Manual Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("Pump1 ON"):
        try:
            requests.get(f"{ESP32_IP}/pump1_on", timeout=5)
            st.success("Pump1 ON")
        except:
            st.error("Error")

    if st.button("Pump1 OFF"):
        try:
            requests.get(f"{ESP32_IP}/pump1_off", timeout=5)
            st.success("Pump1 OFF")
        except:
            st.error("Error")

with col2:
    if st.button("Pump2 ON"):
        try:
            requests.get(f"{ESP32_IP}/pump2_on", timeout=5)
            st.success("Pump2 ON")
        except:
            st.error("Error")

    if st.button("Pump2 OFF"):
        try:
            requests.get(f"{ESP32_IP}/pump2_off", timeout=5)
            st.success("Pump2 OFF")
        except:
            st.error("Error")
