import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- 🔑 CREDENTIALS ---
API_KEY = "YOUR_API_KEY"
MODEL_ID = "smartagri-jaevm/2"

st.set_page_config(page_title="SmartAgri Pro", page_icon="🌿")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 SmartAgri Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>👋 Hello, Roselin Princy!</p>", unsafe_allow_html=True)

# 🌱 Disease Solutions Dictionary
disease_solutions = {
    "healthy": "✅ Your plant is healthy! Maintain proper watering and sunlight.",
    "bacterial spot": "🦠 Remove infected leaves. Use copper-based fungicide. Avoid overhead watering.",
    "early blight": "🍂 Use fungicide sprays. Remove affected leaves. Maintain soil health.",
    "late blight": "⚠️ Remove infected plants immediately. Apply fungicides. Avoid moisture buildup.",
    "leaf mold": "🌫 Improve air circulation. Reduce humidity. Use fungicide if needed.",
    "septoria leaf spot": "🔬 Remove infected leaves. Avoid wet leaves. Apply fungicide.",
    "spider mites": "🕷 Spray neem oil or insecticidal soap. Keep humidity high.",
    "target spot": "🎯 Use resistant varieties. Apply fungicide. Improve spacing.",
    "yellow leaf curl virus": "🦟 Control whiteflies. Remove infected plants immediately."
}

uploaded_file = st.file_uploader("📤 Upload leaf photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🌿 Current Scan", use_container_width=True)
    
    if st.button("🚀 RUN AI DIAGNOSIS"):
        with st.spinner("🤖 AI is analyzing leaf health..."):
            
            # Convert image to Base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            url = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"

            try:
                response = requests.post(
                    url,
                    data=img_str,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                if response.status_code == 200:
                    data = response.json()

                    prediction = data['predictions'][0]['class']
                    confidence = data['predictions'][0]['confidence']

                    st.success(f"🌱 Detected: {prediction}")
                    st.info(f"📊 Confidence: {confidence:.1%}")

                    # 🌿 Get Solution
                    prediction_lower = prediction.lower()
                    solution = disease_solutions.get(
                        prediction_lower,
                        "⚠️ No solution found. Please consult an expert."
                    )

                    st.markdown("### 🩺 Recommended Solution")
                    st.write(solution)

                    # 🎉 Healthy case
                    if "healthy" in prediction_lower:
                        st.balloons()
                    else:
                        st.warning("⚠️ Disease detected! Please follow the solution above.")

                else:
                    st.error(f"❌ Roboflow Error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Processing Error: {e}")
