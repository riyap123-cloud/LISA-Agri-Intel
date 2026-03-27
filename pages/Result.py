import streamlit as st
import sys
import os
import time
import google.generativeai as genai

# Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth_utils import check_authentication
from utils.data_util import save_test_result
from components.navbar import render_navbar
from utils.sms_util import send_test_completion_sms

# Attempt to import gauge, fail silently if not found to prevent crashes
try:
    from components.gauges import create_gauge
except ImportError:
    def create_gauge(val, title):
        st.info(f"Gauge Placeholder: {title} = {val}")

st.set_page_config(page_title="Analysis Results", page_icon="✅", layout="wide")

# --- 🎨 ENTERPRISE BACKGROUND COLOR CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"], [class*="st-"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #F8FAFC; }
    .block-container { padding-top: 2rem !important; max-width: 1000px; }
    
    /* Recommendation Box Style */
    .rec-box {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        border-left: 8px solid #059669; /* Emerald Green */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .rec-box-red { border-left: 8px solid #DC2626; /* Red for deficiency */ }
    
    h1, h2, h3 { color: #0F172A !important; letter-spacing: -0.02em; }
    p { color: #475569 !important; font-size: 1.1rem; }
    
    div.stButton > button { background-color: #0F172A !important; color: white !important; border: none; border-radius: 8px; font-weight: 600; padding: 0.5rem 1rem; transition: all 0.2s; }
    div.stButton > button:hover { background-color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONALITY ---
check_authentication()
render_navbar()

st.title("✅ Analysis Results")

# 1. CHECK FOR DATA (Ensure Processing.py actually ran)
if "analysis_results" not in st.session_state:
    st.warning("No test data found. Please run a test first.")
    if st.button("Go to Test Dashboard"):
        st.switch_page("pages/Test.py")
    st.stop()

# 2. GET REAL CALCULATED DATA FROM PROCESSING.PY
results = st.session_state["analysis_results"]
test_info = st.session_state.get("current_test", {"nutrient": "Fe"})

nutrient_tested = test_info.get("nutrient", "Iron (Fe)")
found_value = results["value"]        # kg/acre
amount_to_add = results["amount_to_add"] # kg/acre
target = results["target"]            # 10 kg/acre

# 3. DETERMINE STATUS
if amount_to_add > 0:
    status = "Deficient"
    status_color = "#DC2626" # Red
    box_class = "rec-box rec-box-red"
    recommendation = f"You need to add <b>{amount_to_add:.2f} kg/acre</b> of {nutrient_tested} fertilizer to reach optimal levels."
else:
    status = "Sufficient"
    status_color = "#059669" # Green
    box_class = "rec-box"
    recommendation = f"Soil {nutrient_tested} levels are optimal. No additional fertilizer is required at this time."

# 4. DISPLAY GAUGE
st.write("---")
create_gauge(found_value, f"{nutrient_tested} Level (kg/acre)")

# 5. DETAILED REPORT
st.markdown(f"""
<div class='{box_class}'>
    <h3 style='margin-top: 0;'>Diagnostic Report</h3>
    <div style='display: flex; justify-content: space-between; margin-top: 20px;'>
        <div>
            <p style='margin: 0; font-size: 0.9rem; color: #64748B;'>Current Level</p>
            <p style='margin: 0; font-size: 1.5rem; font-weight: bold; color: #0F172A;'>{found_value:.2f} <span style='font-size: 1rem; font-weight: normal;'>kg/acre</span></p>
        </div>
        <div>
            <p style='margin: 0; font-size: 0.9rem; color: #64748B;'>Target Level</p>
            <p style='margin: 0; font-size: 1.5rem; font-weight: bold; color: #0F172A;'>{target} <span style='font-size: 1rem; font-weight: normal;'>kg/acre</span></p>
        </div>
        <div>
            <p style='margin: 0; font-size: 0.9rem; color: #64748B;'>Status</p>
            <p style='margin: 0; font-size: 1.5rem; font-weight: bold; color: {status_color};'>{status}</p>
        </div>
    </div>
    <hr style='border: 1px solid #E2E8F0; margin: 20px 0;'>
    <h4 style='color: #0F172A; margin-bottom: 5px;'>Recommendation:</h4>
    <p style='color: #334155;'>{recommendation}</p>
</div>
""", unsafe_allow_html=True)

# --- 5.5 AI SUMMARY (Predictive Crops based on Nutrient) ---
with st.expander("🤖 Generate AI Insights (Gemini)"):
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "your-google-api-key":
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if st.button("Generate AI Summary", use_container_width=True):
            with st.spinner("Analyzing spectral data and generating AI insights..."):
                try:
                    prompt = f"""
                    You are an expert agricultural AI consultant. A farmer has just used an IoT spectrophotometer to test their soil. 

                    Sensor Data:
                    - Nutrient Tested: {nutrient_tested}
                    - Found Value: {found_value} kg/acre
                    - Target Optimal Value: {target} kg/acre
                    - Current Status: {status}
                    - Amount Needed to reach optimal: {amount_to_add} kg/acre

                    Based EXCLUSIVELY on this data, provide a highly professional, concise report containing:
                    1. Current Soil Health Summary: Explain what this {nutrient_tested} level means for the soil.
                    2. Predictive Crop Suggestions: List 3 specific, highly profitable crops that thrive in soil with {found_value} kg/acre of {nutrient_tested}.
                    3. Organic Fertilizer Recommendation: Specific organic ways to add {amount_to_add} kg/acre of {nutrient_tested}.
                    4. Next Steps for the Farmer: 2 bullet points on soil management.

                    Format with clean, bold headings and use professional emojis. Be concise.
                    """
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Failed to generate AI summary: {e}")
    else:
        st.warning("GEMINI_API_KEY is missing or invalid. Please update your Streamlit Secrets.")

# --- 6. SAVE, SMS & HOME BUTTON ---
st.write("---")
if st.button("💾 Save Results, Send SMS & Return", type="primary", use_container_width=True):
    
    farmer_phone = st.session_state.get("phone_number")
    
    # 1. Save the data to the local history database
    save_test_result({
        "crop": "Predictive AI Mode", # Set to this since we removed the crop input
        "nutrient": nutrient_tested, 
        "value": round(found_value, 2), 
        "status": status,
        "recommendation": recommendation
    })
    
    # 2. Send the Twilio SMS Alert
    if farmer_phone:
        success, msg_info = send_test_completion_sms(
            phone_number=farmer_phone,
            crop="Your Farm",
            nutrient=nutrient_tested,
            status=status,
            kg_acre=round(found_value, 2)
        )
        
        if success:
            st.toast("📱 SMS Alert sent to your phone via Twilio!")
        else:
            st.error(f"Failed to send SMS: {msg_info}")
    else:
        st.warning("No phone number found for SMS alert, but results were saved.")
    
    # 3. Brief pause so the user can see the success toast, then route Home
    time.sleep(1.5) 
    st.switch_page("pages/Home.py")