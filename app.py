import streamlit as st
from PIL import Image
import requests
import time

# 1. Page Configuration for a Mobile App Look
st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="centered")

# --- CSS FIX: STOP CUT-OFF & STYLE HEADER ---
st.markdown("""
    <style>
    /* Adds space at the top so the welcome message isn't cut off */
    .main .block-container { 
        padding-top: 3rem !important; 
    }
    /* Styles the welcome message */
    .welcome-header { 
        font-size: 28px !important; 
        font-weight: bold; 
        color: #2E7D32; 
        margin-bottom: 0px; 
    }
    /* Makes buttons large for mobile fingers */
    .stButton>button { 
        width: 100%; 
        height: 3.5em; 
        background-color: #2E7D32; 
        color: white; 
        border-radius: 12px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- WELCOME SECTION ---
st.markdown('<p class="welcome-header">👋 Hello, Roselin Princy!</p>', unsafe_allow_html=True)
st.write("Status: **System Online** | Field: **A1**")

# ESP32 IP - UPDATE THIS with your Serial Monitor IP!
ESP32_IP = "http://http://10.145.234.126" 

# --- SIDEBAR SETTINGS ---
st.sidebar.title("App Settings")
# Use this to CHANGE the result from Healthy to Disease for your demo!
demo_mode = st.sidebar.selectbox("Set AI Result", ["Healthy", "Early Blight", "Aphid Pest"])
page = st.sidebar.radio("Navigation", ["Disease Scanner", "Irrigation Monitor"])

# --- DATA FOR DISEASES ---
database = {
    "Healthy": {"title": "✨ Plant is Healthy", "pesticide": "N/A", "action": "pump_off"},
    "Early Blight": {"title": "⚠️ Tomato Early Blight Detected", "pesticide": "Chlorothalonil Fungicide", "action": "pump_on"},
    "Aphid Pest": {"title": "🚫 Aphid Infestation Detected", "pesticide": "Neem Oil Spray", "action": "pump_on"}
}

# --- FEATURE 1: DISEASE SCANNER ---
if page == "Disease Scanner":
    st.subheader("🌿 AI Crop Disease Scanner")
    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("Analyze & Suggest Treatment"):
            with st.spinner('AI analyzing patterns...'):
                time.sleep(2)
                res = database[demo_mode] # Gets the result you chose in the sidebar
                
                st.divider()
                st.subheader(f"Result: {res['title']}")
                st.info(f"💊 Recommended Treatment: {res['pesticide']}")
                
                if res['action'] == "pump_on":
                    st.warning("Sending Signal to ESP32 Sprayer...")
                    try:
                        requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    except:
                        st.error("ESP32 Offline. Check WiFi connection.")
                else:
                    st.success("Plant status is normal. No action taken.")

# --- FEATURE 2: IRRIGATION MONITOR ---
elif page == "Irrigation Monitor":
    st.subheader("💧 Smart Irrigation Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Soil Moisture", "34%", "-2%")
    col2.metric("Temp", "28°C", "0.5°C")
    
    if st.button("🚿 START MANUAL WATERING"):
        try:
            requests.get(f"{ESP32_IP}/pump_on", timeout=1)
            st.success("Pump Activated")
        except:
            st.error("Hardware Offline")
