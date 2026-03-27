import streamlit as st
from PIL import Image
import requests
import time

# 1. Page Configuration
st.set_page_config(page_title="SmartAgri AI", page_icon="🌿")
st.title("🌿 SmartAgri: AI Disease Scanner")

# 2. ESP32 Configuration - REPLACE 'XX' with your Serial Monitor IP!
ESP32_IP = "http://192.168.1.XX" 

# 3. Disease & Pesticide Database
crop_info = {
    "Disease": {
        "name": "Tomato Late Blight",
        "pesticide": "Copper-based Fungicides (e.g., Kocide 3000)",
        "action": "pump_on"
    },
    "Pest": {
        "name": "Aphid Infestation",
        "pesticide": "Neem Oil or Imidacloprid",
        "action": "pump_on"
    },
    "Healthy": {
        "name": "Healthy Plant",
        "pesticide": "No Pesticide Needed",
        "action": "pump_off"
    }
}

def control_hardware(command):
    try:
        requests.get(f"{ESP32_IP}/{command}", timeout=1)
        st.sidebar.success(f"Signal '{command}' sent to ESP32")
    except:
        st.sidebar.error("ESP32 not found. Check WiFi connection.")

# 4. App UI
uploaded_file = st.file_uploader("Upload a leaf photo...", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Analyzing leaf...', use_column_width=True)
    
    # We use a button to trigger the "Scan" for the demo
    if st.button("Identify Disease & Solution"):
        with st.spinner('AI analyzing patterns...'):
            time.sleep(2) # Simulates AI processing
            
            # For the demo, we show "Disease" results 
            # (You can change "Disease" to "Pest" or "Healthy" to test)
            result = "Disease" 
            info = crop_info[result]
            
            st.divider()
            st.subheader(f"Results: {info['name']}")
            st.write(f"**Recommended Pesticide:** {info['pesticide']}")
            
            if info['action'] == "pump_on":
                st.warning("⚠️ Action Required: Activating ESP32 Sprayer...")
                control_hardware("pump_on")
            else:
                st.success("✨ Plant is safe. No action required.")
                control_hardware("pump_off")
