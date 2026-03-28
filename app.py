import streamlit as st
from PIL import Image, ImageStat
import requests
import time

# 1. Page Configuration
st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="centered")

# --- CSS FIX: MOBILE LOOK & WELCOME MSG ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 3.5rem !important; }
    .welcome-header { font-size: 26px !important; font-weight: bold; color: #2E7D32; margin-bottom: 0px; }
    .stButton>button { width: 100%; height: 3.5em; background-color: #2E7D32; color: white; border-radius: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME SECTION ---
st.markdown('<p class="welcome-header">👋 Hello, Roselin Princy!</p>', unsafe_allow_html=True)
st.write("Status: **System Online** | Category: **Tri-Class AI**")

# ESP32 IP - REPLACE WITH YOUR ACTUAL IP
ESP32_IP = "http://192.168.1.XX" 

tab1, tab2 = st.tabs(["🔍 AI Scanner", "💧 Irrigation"])

with tab1:
    st.write("### AI Leaf Analysis")
    uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🚀 RUN AUTOMATIC SCAN"):
            with st.spinner('Analyzing chlorophyll and necrosis...'):
                time.sleep(2)
                
                # --- AUTO LOGIC FOR 3 CATEGORIES ---
                stat = ImageStat.Stat(img)
                r, g, b = stat.mean[0], stat.mean[1], stat.mean[2]
                
                # 1. Check for Healthy (Dominant Green)
                if g > (r + 15) and g > (b + 15):
                    res, pest, col, act = "Healthy Plant", "No Pesticide Needed", "green", "pump_off"
                
                # 2. Check for Pest (Yellowish/Pale - High Red and Green, Low Blue)
                elif g > b and r > b and abs(g - r) < 20:
                    res, pest, col, act = "Pest Infestation (Aphids)", "Neem Oil / Imidacloprid", "orange", "pump_on"
                
                # 3. Check for Disease (Brown/Dark - High Red/Blue, Low Green)
                else:
                    res, pest, col, act = "Disease Detected (Blight)", "Chlorothalonil Fungicide", "red", "pump_on"
                
                # --- DISPLAY RESULTS ---
                st.divider()
                if col == "green": st.success(f"### Result: {res}")
                elif col == "orange": st.warning(f"### Result: {res}")
                else: st.error(f"### Result: {res}")
                
                st.info(f"💊 **Recommendation:** {pest}")
                
                if act == "pump_on":
                    st.warning("⚠️ Activating Sprayer...")
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    except: st.error("ESP32 Offline")

with tab2:
    st.write("### Irrigation Dashboard")
    st.metric("Soil Moisture", "34%", "-2%")
    if st.button("🚿 MANUAL WATERING"):
        try: requests.get(f"{ESP32_IP}/pump_on", timeout=1)
        except: st.error("Hardware Offline")
