import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- 🔑 CREDENTIALS ---
# Replace with the Private Key starting with cSRH from your Settings
API_KEY = "cSRHsMa3Pl9RnYyvIIH6" 
MODEL_ID = "smartagri-jaevm/2" 
ESP32_IP = "http://10.145.234.126" 

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload leaf photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Current Scan", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("AI is analyzing leaf health..."):
            # 1. Convert image to Base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # 2. Classification API URL
            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
            
            try:
                response = requests.post(url, data=img_str, headers={"Content-Type": "application/x-www-form-urlencoded"})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- FIXED EXTRACTION LOGIC ---
                    # Classification models return 'predictions' as a dictionary
                    prediction = data['top']
                    confidence = data['predictions'][prediction]['confidence']

                    st.success(f"### Result: {prediction}")
                    st.info(f"AI Confidence: {confidence:.1%}")

                    # 3. Hardware Logic
                    if "healthy" not in prediction.lower():
                        st.warning("🚨 Alert: Disease detected! Activating Sprayer...")
                        # requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    else:
                        st.balloons()
                else:
                    st.error(f"Roboflow Error: {response.status_code}")
            except Exception as e:
                # This specifically catches the 'list index' error from your screenshot
                st.error(f"Processing Error: {e}")
                st.write("The AI returned data, but the format was unexpected. Check your Model Type.")

with st.expander("🛠️ Manual Hardware Controls"):
    st.button("🚿 Test Pump ON")
