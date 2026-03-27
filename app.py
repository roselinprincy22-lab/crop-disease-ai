import streamlit as st
from PIL import Image
import requests
import time
import pandas as pd

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="wide")

# ESP32 IP - UPDATE THIS!
ESP32_IP = "http://192.168.1.XX" 

# --- NAVIGATION ---
page = st.sidebar.selectbox("Select Feature", ["Disease Scanner", "Irrigation Monitor"])

# --- FEATURE 1: DISEASE SCANNER ---
if page == "Disease Scanner":
    st.title("🌿 AI Disease & Pesticide Scanner")
    
    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_column_width=True)
        
        if st.button("Analyze & Suggest Treatment"):
            with st.spinner('AI Processing...'):
                time.sleep(2)
                # Mock result for demo
                st.subheader("Result: Tomato Early Blight")
                st.error("💊 Recommended Pesticide: Chlorothalonil or Copper Fungicide")
                if st.button("Start Emergency Spray"):
                    requests.get(f"{ESP32_IP}/pump_on")

# --- FEATURE 2: IRRIGATION MONITOR ---
elif page == "Irrigation Monitor":
    st.title("💧 Real-time Irrigation Dashboard")
    
    # Create 3 columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # In a real app, you'd fetch this from ESP32. For the demo:
    moisture = 35 
    temp = 28
    
    col1.metric("Soil Moisture", f"{moisture}%", "-5%")
    col2.metric("Temperature", f"{temp}°C", "1.2°C")
    col3.metric("Status", "Dry", delta_color="inverse")

    if st.button("Manual Irrigation ON"):
        try:
            requests.get(f"{ESP32_IP}/pump_on")
            st.success("Pump Activated")
        except:
            st.error("Hardware Offline")

    # Add a data table like your Zoho version had
    st.write("### Field History")
    df = pd.DataFrame({
        "Farmer": ["Ravi Kumar", "Suresh"],
        "Field ID": ["FLD01", "FLD02"],
        "Moisture": [35, 20],
        "Status": ["Active", "Needs Water"]
    })
    st.table(df)
