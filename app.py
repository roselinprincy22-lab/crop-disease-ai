import streamlit as st
import requests
from PIL import Image
import io

# --- 🔑 YOUR FINAL CREDENTIALS ---
# Make sure this is the PRIVATE key from your Settings -> API Keys page
API_KEY = "cSRHsMa3Pl9RnYyvIIH6" 
MODEL_ID = "smartagri-jaevm/2" 
ESP32_IP = "http://10.145.234.126" # Replace XX with your ESP32's actual IP

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

# Custom CSS for a better mobile look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2E7D32; color: white; height: 3em; font-weight: bold; }
    .reportview-container { background: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 SmartAgri Pro")
st.subheader("👋 Hello, Roselin Princy!")
st.write("Upload a leaf photo to begin the AI health check.")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Leaf", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("AI analyzing dataset..."):
            # Prepare image bytes
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            img_bytes = buf.getvalue()

            # Roboflow Classification URL
            # We use the 'classify' endpoint for your type of project
            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
            
            try:
                response = requests.post(url, data=img_bytes, headers={"Content-Type": "application/x-www-form-urlencoded"})
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result['top']
                    confidence = result['predictions'][prediction]['confidence']
                    
                    st.divider()
                    st.success(f"### Result: {prediction}")
                    st.info(f"Confidence Level: {confidence:.1%}")

                    # HARDWARE TRIGGER
                    if "healthy" not in prediction.lower():
                        st.warning("🚨 Alert: Disease/Pest detected! Activating Sprayer...")
                        # requests.get(f"{ESP32_IP}/pump_on", timeout=1)
                    else:
                        st.balloons()
                        st.write("✅ Plant is in great health!")
                else:
                    st.error(f"Error: {response.status_code}. Please check if your API Key is correct.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with st.expander("🛠️ Manual Hardware Controls"):
    if st.button("🚿 Test Pump ON"):
        try: requests.get(f"{ESP32_IP}/pump_on")
        except: st.error("ESP32 Not Found")
