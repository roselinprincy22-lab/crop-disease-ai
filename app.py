import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import requests

# Set up the Page Header
st.set_page_config(page_title="SmartAgri AI", page_icon="🌿")
st.title("🌿 SmartAgri: AI Disease Scanner")

# Function to load the Teachable Machine model
@st.cache_resource
def load_model():
    # VERIFY: Ensure these filenames match your renamed GitHub files exactly
    model = tf.keras.models.load_model("model.json", compile=False)
    return model

# Function to send signal to ESP32
def control_esp32(state):
    esp32_url = "http://http://10.145.234.191:5000/predict" # Replace with your ESP32 IP address
    try:
        requests.get(f"{esp32_url}/{state}", timeout=2)
        st.sidebar.success(f"ESP32 Status: {state.upper()} sent")
    except:
        st.sidebar.error("ESP32 Offline")

# Load model and labels
model = load_model()
# VERIFY: These must match the labels from your Teachable Machine project
class_names = ["Healthy", "Disease", "Pest"]
# Image Upload UI
file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png"])

if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    
    # Pre-process image for AI (224x224 is standard for TM)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image)
    normalized_img_array = (img_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_img_array

    # Prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    label = class_names[index]
    confidence = prediction[0][index]

    st.write(f"### Diagnosis: {label}")
    st.write(f"**Confidence:** {round(confidence * 100, 2)}%")

    # Hardware Integration logic
    if label == "Disease":
        st.warning("⚠️ Disease found! Activating Sprayer...")
        control_esp32("on")
    else:
        st.success("✨ Plant is healthy.")
        control_esp32("off")
