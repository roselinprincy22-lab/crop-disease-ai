import streamlit as st
import requests
from PIL import Image
import io

# 🔑 SETTINGS
API_KEY = "cSRHsMa3Pl9RnYyvIIH6"
MODEL_ID = "smartagri-jaevm/2"
ESP32_IP = "http://10.145.234.126" 

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")
st.title("🌿 SmartAgri Pro")

# --- DIAGNOSIS SECTION ---
uploaded_file = st.file_uploader("📤 Upload leaf image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    if st.button("🚀 Diagnose"):
        # ... (Your Roboflow Request Code here) ...
        # Assume 'prediction' is the result from Roboflow
        
        prediction_clean = prediction.strip().lower()
        
        if "healthy" in prediction_clean:
            st.balloons() # 🎈 Flying Balloons!
            st.success("✅ Plant is Healthy!")
        else:
            st.error(f"⚠️ Disease Detected: {prediction}")
            # Auto-trigger pump for sick plants
            try:
                requests.get(f"{ESP32_IP}/pump1_on", timeout=2)
            except:
                pass

# --- SENSOR SECTION ---
st.header("🌡️ Live Sensor Data")
if st.button("📡 Get Sensor Data"):
    try:
        # We use a 5-second timeout because 10.x.x.x networks can be slow
        res = requests.get(f"{ESP32_IP}/data", timeout=5)
        if res.status_code == 200:
            val = res.json().get("soil")
            st.metric("Soil Moisture", val)
            st.success("Data Received!")
    except Exception as e:
        st.error(f"Still failing? Try opening {ESP32_IP}/data in your browser.")
