import streamlit as st
import requests

ESP32_IP = "http://10.145.234.126"  # change this

session = requests.Session()
session.trust_env = False

st.title("🌱 Sensor Data")

if st.button("Get Sensor Data"):
    try:
        res = session.get(f"{ESP32_IP}/data", timeout=5)

        if res.status_code == 200:
            data = res.json()
            soil = data["soil"]

            st.success("Connected ✅")
            st.metric("Soil Moisture", soil)

            if soil > 3000:
                st.warning("Dry Soil")
            else:
                st.success("Soil Good")

    except Exception as e:
        st.error(f"Connection Failed: {e}")
