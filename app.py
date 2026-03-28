import streamlit as st
import requests
from PIL import Image
import io

# --- ⚙️ CONFIGURATION (Update your Private Key here) ---
# Use the Private API Key starting with cSRH... from your last screenshot
API_KEY = "cSRHsMa3Pl9RnYyvIIH6" 
MODEL_ID = "smartagri-jaevm/2"
ESP32_IP = "http://10.145.234.126" # Replace XX with your ESP32's actual IP

# --- 🎨 PAGE STYLING ---
st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
        border: none;
    }
    .welcome-text {
        text-align: center;
        color: #1B5E20;
        font-family: 'sans-serif';
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🏠 HEADER ---
st.markdown("<h1 class='welcome-text'>👋 Hello, Roselin Princy!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-Powered Plant Health Guardian</p>", unsafe_allow_html=True)
st.write("---")

# --- 📸 SCANNER SECTION ---
st.subheader("🔍 Leaf Disease Scanner")
uploaded_file = st.file_uploader("Choose a leaf photo...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Leaf", use_container_width=True)
    
    # Analyze Button
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("Analyzing dataset of 7,897 images..."):
            try:
                # 1. Prepare Image for Roboflow
                buf = io.BytesIO()
                image.save(buf, format="JPEG")
                img_bytes = buf.getvalue()

                # 2. Call Roboflow Classification API
                url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"
                response = requests.post(url, data=img_bytes, headers={"Content-Type": "application/x-www-form-urlencoded"})
                
                if response.status_code == 200:
                    data = response.json()
                    prediction = data['top']
                    confidence = data['predictions'][prediction]['confidence']

                    # 3. Display Results
                    st.divider()
                    st.metric(label="Detected Condition", value=prediction)
                    st.write(f"**Confidence Level:** {confidence:.2%}")

                    # 4. Hardware Logic (ESP32)
                    if "healthy" in prediction.lower():
                        st.success("✅ Plant is healthy. No treatment required.")
                        # requests.get(f"{ESP32_IP}/pump_off", timeout=2) 
                    else:
                        st.error(f"🚨 Disease Detected: {prediction}")
                        st.warning("⚠️ Action: Initiating ESP32 Spraying System...")
                        # Try to trigger the pump
                        try:
                            requests.get(f"{ESP32_IP}/pump_on", timeout=2)
                            st.info("💧 Pump is now active.")
                        except:
                            st.caption("Note: Hardware offline or IP mismatch.")
                else:
                    st.error("AI Service Error. Please check your API Key.")
            
            except Exception as e:
                st.error(f"Error: {e}")

# --- 💧 MANUAL OVERRIDE ---
st.write("---")
with st.expander("🛠️ Manual Hardware Controls"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚿 Pump ON"):
            try: requests.get(f"{ESP32_IP}/pump_on")
            except: st.error("Offline")
    with col2:
        if st.button("🛑 Pump OFF"):
            try: requests.get(f"{ESP32_IP}/pump_off")
            except: st.error("Offline")

st.caption("SmartAgri System v2.0 | Developed by Roselin Princy")
