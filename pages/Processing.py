import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import sys
import os

# --------------------------------------------------
# PATH FIX
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth_utils import check_authentication
from components.navbar import render_navbar

# --------------------------------------------------
# 🌐 CONFIG
# --------------------------------------------------
THINGSPEAK_CHANNEL_ID = "3313044"
THINGSPEAK_READ_API_KEY = "VBG0EKERHSP7MO9J"

THINGSPEAK_READ_URL = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds/last.json?api_key={THINGSPEAK_READ_API_KEY}"

ESP_IP = "http://10.135.205.239"

# --------------------------------------------------
# page CONFIG
# --------------------------------------------------
st.set_page_config(page_title="LISA Processing", page_icon="⚙️", layout="wide")
check_authentication()
render_navbar()

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    div.stButton > button[kind="primary"] { background-color: #059669 !important; color: white !important; border: none; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "current_test" not in st.session_state:
    st.error("⚠️ No active test found. Please start from the Test Dashboard.")
    st.stop()

if "proc_step" not in st.session_state:
    st.session_state["proc_step"] = 1

# --------------------------------------------------
# 🔥 ESP TRIGGER FUNCTION (FINAL FIX)
# --------------------------------------------------
def trigger_esp(measure_type):
    try:
        url = f"{ESP_IP}/read?type={measure_type}"
        r = requests.get(url, timeout=30)
        r.close()  # ✅ prevent connection leak
        return True
    except Exception as e:
        st.error(f"❌ ESP Error: {e}")
        return False

# --------------------------------------------------
# ☁️ FETCH FROM THINGSPEAK (FINAL SAFE VERSION)
# --------------------------------------------------
def fetch_sensor_data():
    try:
        response = requests.get(THINGSPEAK_READ_URL, timeout=5)

        if response.status_code == 200:
            data = response.json()

            g = float(data.get("field1") or 0.0001)
            o = float(data.get("field2") or 0.0001)
            ir = float(data.get("field3") or 0.0001)

            return {
                "Green": g,
                "Orange": o,
                "IR": ir,
            }
        else:
            st.error("❌ ThingSpeak error")
            return None

    except Exception as e:
        st.error(f"⚠️ {e}")
        return None

# ==================================================
# STEP 1: Io
# ==================================================
if st.session_state["proc_step"] == 1:
    st.title("💧 Calibration Phase (1/3)")
    st.progress(33)
    st.info("Insert the CLEAR BLANK SOLUTION.")

    if st.button("🔴 Capture Calibration (Io)", use_container_width=True):

        with st.spinner("Measuring I0... Please wait (20 sec)"):
            if trigger_esp("I0"):

                time.sleep(20)  # 🔥 FULL SAFE DELAY

                io_data = fetch_sensor_data()

                if io_data:
                    st.session_state["Io_data"] = io_data
                    st.success("Calibration captured!")
                    time.sleep(1)
                    st.session_state["proc_step"] = 2
                    st.rerun()
            else:
                st.error("❌ ESP not reachable. Check if your laptop and ESP are on the same Wi-Fi.")

# ==================================================
# STEP 2: I
# ==================================================
elif st.session_state["proc_step"] == 2:
    st.title("🧪 Measurement Phase (2/3)")
    st.progress(66)
    st.warning("Insert the TREATED SOIL SAMPLE.")

    if st.button("🟢 Capture Sample (I)", use_container_width=True):

        with st.spinner("Measuring Sample... Please wait (20 sec)"):
            if trigger_esp("I"):

                time.sleep(20)

                i_data = fetch_sensor_data()

                if i_data:
                    st.session_state["I_data"] = i_data
                    st.success("Sample captured!")
                    time.sleep(1)
                    st.session_state["proc_step"] = 3
                    st.rerun()
            else:
                st.error("❌ ESP not reachable.")

# ==================================================
# STEP 3: PROCESSING
# ==================================================
elif st.session_state["proc_step"] == 3:
    st.title("⚙️ Processing (3/3)")
    st.progress(100)

    Io = st.session_state["Io_data"]
    I_val = st.session_state["I_data"]

    # --- 🛠️ DEBUG WINDOW ---
    st.info(f"🔍 **Debug - Calibration (Io):** Green={Io['Green']}, IR={Io['IR']}")
    st.info(f"🔍 **Debug - Soil Sample (I):** Green={I_val['Green']}, IR={I_val['IR']}")

    # Safe calculation
    try:
        # Prevent division by zero
        safe_I_green = I_val["Green"] if I_val["Green"] > 0 else 0.0001
        safe_I_ir = I_val["IR"] if I_val["IR"] > 0 else 0.0001

        # Calculate raw absorbances (allowing negative numbers temporarily for debugging)
        abs_green = np.log10(Io["Green"] / safe_I_green)
        abs_ir = np.log10(Io["IR"] / safe_I_ir)

        # Turbidity Compensation
        Ar = abs_green - abs_ir
        
        # Now apply physical limits (Absorbance can't be practically negative)
        Ar_final = max(Ar, 0)

        ppm_value = Ar_final / 0.198
        kg_per_acre = ppm_value * 0.907

        TARGET = 10.0
        amount_to_add = max(TARGET - kg_per_acre, 0)

        # Save for the Results page
        st.session_state["analysis_results"] = {
            "value": round(kg_per_acre, 2),
            "amount_to_add": round(amount_to_add, 2),
            "target": TARGET,
            "Ar": round(Ar_final, 4),
            "ppm": round(ppm_value, 2)
        }

        st.success("Analysis Complete!")

        st.write("### 📊 Raw Mathematical Results")
        st.write(f"- **Green Absorbance:** {round(abs_green, 4)}")
        st.write(f"- **IR Absorbance:** {round(abs_ir, 4)}")
        st.write(f"- **Final Compensated Absorbance (Ar):** {round(Ar_final, 4)}")
        
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart Test", use_container_width=True):
                st.session_state["proc_step"] = 1
                st.rerun()
        with col2:
            if st.button("📄 Generate Final AI Report ➔", type="primary", use_container_width=True):
                st.session_state["proc_step"] = 1
                st.switch_page("pages/Result.py")

    except Exception as e:
        st.error(f"Calculation error: {e}")