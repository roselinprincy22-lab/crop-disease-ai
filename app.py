import streamlit as st
from PIL import Image
import requests
import time

# 1. Page Configuration for Mobile
st.set_page_config(
    page_title="SmartAgri Pro", 
    page_icon="🌿", 
    layout="centered", # 'centered' looks more like an app than 'wide'
    initial_sidebar_state="collapsed" # Hides sidebar on mobile for a cleaner look
)

# --- CUSTOM APP LOOK (CSS) ---
st.markdown("""
    <style>
    /* Makes buttons bigger and easier to touch on mobile */
    .stButton>button {
        width: 100%;
        height: 3em;
        border-radius: 10px;
        background-color: #2E7D32;
        color: white;
    }
    /* Removes empty top padding */
    .block-container {
        padding-top: 1rem;
    }
    /* Fixes visibility of buttons on mobile */
    div.stButton {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME SECTION ---
# This mimics the "Hello, Roselin Princy" from your Zoho version
st.subheader("👋 Welcome, Roselin Princy!")
st.write("SmartAgri is monitoring your fields.")

# ESP32 IP
ESP32_IP = "http://http://10.145.234.126" 

# --- APP TABS (Navigation at the top for Mobile) ---
tab1, tab2 = st.tabs(["🔍 Disease Scanner", "💧 Irrigation"])

# --- TAB 1: DISEASE SCANNER ---
with tab1:
    st.write("### AI Crop Scanner")
    uploaded_file = st.file_uploader("Take a photo of the leaf", type=["jpg", "png"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        # This button is now forced to be visible via the CSS above
        if st.button("🚀 IDENTIFY DISEASE"):
            with st.spinner('Analyzing...'):
                time.sleep(2)
                st.success("Result: Tomato Early Blight")
                st.warning("💊 Suggestion: Chlorothalonil Spray")
                
                if st.button("Confirm & Start Sprayer"):
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                        st.sidebar.write("Signal Sent!")
                    except:
                        st.error("ESP32 Connection Error")

# --- TAB 2: IRRIGATION ---
with tab2:
    st.write("### Field Status")
    col1, col2 = st.columns(2)
    col1.metric("Moisture", "32%", "-2%")
    col2.metric("Temp", "29°C", "0.5°C")
    
    if st.button("🚿 START MANUAL WATERING"):
         requests.get(f"{ESP32_IP}/pump_on")
