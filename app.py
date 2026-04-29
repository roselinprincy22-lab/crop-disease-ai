import streamlit as st
import requests
from PIL import Image

# --- 🔑 CREDENTIALS ---
API_KEY = "YOUR_API_KEY"
MODEL_ID = "smartagri-jaevm/2"

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.title("🌿 SmartAgri Pro")

uploaded_file = st.file_uploader("📤 Upload leaf photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🌿 Current Scan", use_container_width=True)

    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("🤖 AI is analyzing..."):

            url = "https://serverless.roboflow.com/infer/workflows"

            try:
                response = requests.post(
                    url,
                    files={"file": uploaded_file},
                    data={
                        "api_key": API_KEY,
                        "model_id": MODEL_ID
                    }
                )

                data = response.json()
                st.write("DEBUG:", data)  # remove later

                if "predictions" in data and len(data["predictions"]) > 0:
                    prediction = data["predictions"][0]["class"]
                    confidence = data["predictions"][0]["confidence"]

                    st.success(f"🌱 Detected: {prediction}")
                    st.info(f"📊 Confidence: {confidence:.1%}")

                else:
                    st.warning("⚠️ No predictions found")

            except Exception as e:
                st.error(f"❌ Error: {e}")
