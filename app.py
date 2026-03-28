import streamlit as st
import requests
from PIL import Image
import io

# --- ⚙️ CONFIGURATION ---
# IMPORTANT: Click the 'Eye' icon in Roboflow to see the full key before copying!
API_KEY = "cSRHsMa3Pl9RnYyvIIH6" 
MODEL_ID = "smartagri-jaevm/2"
ESP32_IP = "http://10.145.234.126" # Replace XX with your ESP32's actual IP

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

# --- UI DESIGN ---
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload leaf photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Leaf", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("AI is analyzing leaf health..."):
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            img_bytes = buf.getvalue()

            # Using the direct classification endpoint
            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
            
            try:
                response = requests.post(url, data=img_bytes, headers={"Content-Type": "application/x-www-form-urlencoded"})
                
                if response.status_code == 200:
                    data = response.json()
                    prediction = data['top']
                    confidence = data['predictions'][prediction]['confidence']

                    st.success(f"### Result: {prediction}")
                    st.info(f"Confidence Level: {confidence:.1%}")

                    if "healthy" in prediction.lower():
                        st.balloons()
                        st.write("✅ Plant is healthy!")
                    else:
                        st.error(f"🚨 {prediction} detected!")
                        st.warning("Action: Activating ESP32 Spray System...")
                        # requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                elif response.status_code == 401:
                    st.error("Invalid API Key. Please re-copy the Private API Key from Roboflow.")
                elif response.status_code == 404:
                    st.error("Model not found. Check if your Model ID is 'smartagri-jaevm/2'.")
                else:
                    st.error(f"Server Error {response.status_code}: Check if the model is fully trained.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with st.expander("🛠️ Manual Hardware Controls"):
    st.button("🚿 Test Pump ON")
