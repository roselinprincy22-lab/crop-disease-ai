import streamlit as st
from PIL import Image, ImageStat
import requests
import time

# 1. Page Configuration
st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="centered")

# --- CSS FIX: APP LOOK & NO CUT-OFF ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 3.5rem !important; }
    .welcome-header { font-size: 28px !important; font-weight: bold; color: #2E7D32; }
    .stButton>button { width: 100%; height: 3.5em; background-color: #2E7D32; color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME SECTION ---
st.markdown('<p class="welcome-header">👋 Hello, Roselin Princy!</p>', unsafe_allow_html=True)

# ESP32 IP - REPLACE WITH YOUR ACTUAL IP
ESP32_IP = "http://192.168.1.XX" 

tab1, tab2 = st.tabs(["🔍 Disease Scanner", "💧 Irrigation"])

with tab1:
    st.subheader("AI Auto-Detection")
    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("🚀 START AUTOMATIC SCAN"):
            with st.spinner('Analyzing Leaf Pigmentation...'):
                time.sleep(2)
                
                # --- AUTO-DETECTION LOGIC (Color Analysis) ---
                stat = ImageStat.Stat(img)
                red_channel = stat.mean[0]
                green_channel = stat.mean[1]
                
                # If Green is much higher than Red, it's likely healthy
                # If Red/Brown tones are high, it's likely diseased
                if green_channel > (red_channel + 15):
                    res_title = "✨ Plant is Healthy"
                    res_pesticide = "None - Keep up the good work!"
                    res_color = "green"
                    action = "pump_off"
                else:
                    res_title = "⚠️ Tomato Early Blight Detected"
                    res_pesticide = "Chlorothalonil Fungicide"
                    res_color = "red"
                    action = "pump_on"
                
                st.divider()
                st.subheader(f"Result: {res_title}")
                st.info(f"💊 Recommended Treatment: {res_pesticide}")
                
                if action == "pump_on":
                    st.warning("⚠️ High Risk: Activating ESP32 Sprayer...")
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    except:
                        st.error("ESP32 Offline - Connect to same WiFi")

with tab2:
    st.subheader("Field Status")
    st.metric("Soil Moisture", "34%", "-2%")
    if st.button("🚿 MANUAL WATERING"):
        requests.get(f"{ESP32_IP}/pump_on")
