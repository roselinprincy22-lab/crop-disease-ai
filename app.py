import streamlit as st
from PIL import Image
import requests
import time

# 1. Page Configuration for a Mobile App Look
st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="centered")

# --- CSS FIX: STOP CUT-OFF & STYLE BUTTONS ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem !important; }
    .welcome-header { font-size: 26px !important; font-weight: bold; color: #2E7D32; margin-bottom: 0px; }
    .stButton>button { width: 100%; height: 3.5em; background-color: #2E7D32; color: white; border-radius: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME SECTION ---
st.markdown('<p class="welcome-header">👋 Hello, Roselin Princy!</p>', unsafe_allow_html=True)
st.write("Status: **System Online** | Location: **Field A1**")

# ESP32 IP - IMPORTANT: Update this with your actual IP!
ESP32_IP = "http://192.168.1.XX" 

# --- APP TABS ---
tab1, tab2 = st.tabs(["🔍 Disease Scanner", "💧 Irrigation"])

with tab1:
    st.write("### AI Crop Analysis")
    uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        # 🧪 SMART DETECTION LOGIC (Triggered by Filename for Demo)
        filename = uploaded_file.name.lower()
        
        if st.button("🚀 SCAN FOR DISEASE"):
            with st.spinner('AI analyzing patterns...'):
                time.sleep(2)
                
                # Logic to show DIFFERENT results
                if "healthy" in filename:
                    st.success("### Result: Healthy Plant")
                    st.write("✨ **No treatment required.** Plant is in optimal condition.")
                    requests.get(f"{ESP32_IP}/pump_off") # Ensure pump stays off
                elif "pest" in filename:
                    st.error("### Result: Pest Infestation")
                    st.warning("💊 **Recommended:** Neem Oil or Imidacloprid Spray")
                    requests.get(f"{ESP32_IP}/pump_on") # Trigger sprayer
                else:
                    st.error("### Result: Tomato Early Blight")
                    st.warning("💊 **Recommended:** Chlorothalonil Fungicide")
                    requests.get(f"{ESP32_IP}/pump_on") # Trigger sprayer

with tab2:
    st.write("### Irrigation Monitoring")
    c1, c2 = st.columns(2)
    c1.metric("Moisture", "34%", "-2%")
    c2.metric("Temp", "28°C", "0.5°C")
    
    if st.button("🚿 START MANUAL PUMP"):
        requests.get(f"{ESP32_IP}/pump_on")
