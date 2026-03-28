import streamlit as st
from PIL import Image
import requests
import time

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="wide")

# ESP32 IP - IMPORTANT: Update with your actual ESP32 IP!
ESP32_IP = "http://10.145.234.126" 

# --- SIDEBAR SETTINGS ---
st.sidebar.title("App Settings")
# This hidden selector lets you "force" the result for your presentation demo
demo_mode = st.sidebar.selectbox("Test AI Result", ["Healthy", "Early Blight", "Aphid Pest"])
page = st.sidebar.radio("Navigation", ["Disease Scanner", "Irrigation Monitor"])

# --- DATA FOR DISEASES ---
database = {
    "Healthy": {"title": "✨ Plant is Healthy", "pesticide": "N/A", "color": "green", "action": "pump_off"},
    "Early Blight": {"title": "⚠️ Tomato Early Blight Detected", "pesticide": "Chlorothalonil or Copper Fungicide", "color": "red", "action": "pump_on"},
    "Aphid Pest": {"title": "🚫 Aphid Infestation Detected", "pesticide": "Neem Oil or Imidacloprid Spray", "color": "orange", "action": "pump_on"}
}

# --- FEATURE 1: DISEASE SCANNER ---
if page == "Disease Scanner":
    st.title("🌿 AI Crop Disease Scanner")
    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("Analyze & Suggest Treatment"):
            with st.spinner('AI analyzing patterns...'):
                time.sleep(2) # Fake processing time
                res = database[demo_mode]
                st.subheader(f"Result: {res['title']}")
                st.info(f"💊 Recommended Treatment: {res['pesticide']}")
                
                if res['action'] == "pump_on":
                    st.warning("Sending Signal to ESP32 Sprayer...")
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    except:
                        st.error("ESP32 Offline")
                else:
                    st.success("Plant status is normal.")

# --- FEATURE 2: IRRIGATION MONITOR ---
elif page == "Irrigation Monitor":
    st.title("💧 Smart Irrigation Dashboard")
    # ... (Keep your previous dashboard code here)
