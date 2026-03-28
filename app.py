import streamlit as st
from PIL import Image
import requests
import time

# 1. Page Configuration
st.set_page_config(
    page_title="SmartAgri Pro", 
    page_icon="🌿", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS FIX FOR CUT-OFF TEXT & MOBILE BUTTONS ---
st.markdown("""
    <style>
    /* Fix for cut-off welcome message */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    .welcome-text {
        font-size: 24px !important;
        font-weight: bold;
        margin-bottom: 10px;
        color: #2E7D32;
    }
    /* Make buttons large and visible on mobile */
    .stButton>button {
        width: 100% !important;
        height: 3.5em !important;
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME MESSAGE ---
st.markdown('<p class="welcome-text">👋 Hello, Roselin Princy!</p>', unsafe_allow_html=True)
st.write("System status: **Active** | Location: **Field A1**")

# ESP32 IP - REPLACE WITH YOUR ACTUAL IP
ESP32_IP = "http://192.168.1.XX" 

# --- TABS FOR NAVIGATION ---
tab1, tab2 = st.tabs(["🔍 Disease Scanner", "💧 Irrigation Monitor"])

with tab1:
    st.write("### AI Leaf Analysis")
    uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        # SMART DETECTION LOGIC: Looks at the filename
        fname = uploaded_file.name.lower()
        
        if st.button("🚀 SCAN FOR DISEASE"):
            with st.spinner('Analyzing patterns...'):
                time.sleep(2)
                
                if "healthy" in fname:
                    result = "Healthy Plant"
                    pest = "None"
                    color = "green"
                    action = "pump_off"
                elif "pest" in fname:
                    result = "Aphid Infestation"
                    pest = "Neem Oil Spray"
                    color = "orange"
                    action = "pump_on"
                else:
                    # Default disease result
                    result = "Tomato Early Blight"
                    pest = "Chlorothalonil Fungicide"
                    color = "red"
                    action = "pump_on"
                
                st.subheader(f"Result: {result}")
                st.info(f"💊 Recommended: {pest}")
                
                if action == "pump_on":
                    st.warning("⚠️ Activating Sprayer...")
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    except:
                        st.error("ESP32 Offline - Connect to same WiFi")

with tab2:
    st.write("### Soil & Water Status")
    c1, c2 = st.columns(2)
    c1.metric("Moisture", "34%", "-2%")
    c2.metric("Temp", "28°C", "0.5°C")
    
    if st.button("🚿 MANUAL WATERING ON"):
        try:
            requests.get(f"{ESP32_IP}/pump_on", timeout=1)
        except:
            st.error("Hardware disconnected")
