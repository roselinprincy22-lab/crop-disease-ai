import streamlit as st
import requests
from PIL import Image
import io

# --- 🔑 CREDENTIALS (RE-COPY FROM ROBOLFLOW) ---
# Use the Private API Key from Settings -> API Keys (starts with cSRH)
API_KEY = "cSRHsMa3Pl9RnYyvIIH6" 
MODEL_ID = "smartagri-jaevm/2" 
ESP32_IP = "http://10.145.234.126" # Replace XX with your ESP32's actual IP

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

# Custom UI Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background-color: #2E7D32; color: white; height: 3.5em; font-weight: bold; }
    .main-title { text-align: center; color: #1B5E20; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload leaf photo to scan...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Current Scan", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("Analyzing image..."):
            # Prepare image bytes for the API
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            img_bytes = buf.getvalue()

            # The direct URL for Classification models
            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
            
            try:
                response = requests.post(url, data=img_bytes, headers={"Content-Type": "application/x-www-form-urlencoded"})
                
                if response.status_code == 200:
                    data = response.json()
                    # Extracting results from your ResNet18 model
                    prediction = data['top']
                    confidence = data['predictions'][prediction]['confidence']
                    
                    st.divider()
                    st.success(f"### Result: {prediction}")
                    st.metric(label="AI Confidence", value=f"{confidence:.1%}")

                    # --- HARDWARE CONTROL ---
                    if "healthy" in prediction.lower():
                        st.balloons()
                        st.info("✨ Plant is healthy! No spray needed.")
                    else:
                        st.error(f"🚨 ALERT: {prediction} detected!")
                        st.warning("💊 Action: Activating ESP32 local sprayer...")
                        # requests.get(f"{ESP32_IP}/pump_on", timeout=1) 
                else:
                    st.error(f"Roboflow Error: {response.status_code}")
                    st.caption(f"Details: {response.text}")
            except Exception as e:
                st.error(f"App Error: {e}")

st.write("---")
with st.expander("🛠️ Manual Hardware Controls"):
    st.button("🚿 Test Pump ON")
