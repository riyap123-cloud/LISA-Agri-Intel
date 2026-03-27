import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth_utils import check_authentication
from components.navbar import render_navbar

st.set_page_config(page_title="New Test", page_icon="🧪", layout="wide")

# --- 🎨 ENTERPRISE SAAS UI DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background-color: #F8FAFC; 
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 900px; /* Slightly narrower for forms */
    }

    /* Style the form container */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    h1 { color: #0F172A !important; letter-spacing: -0.02em; }
    p { color: #475569 !important; }
    label { font-weight: 500 !important; color: #1E293B !important; }

    /* Primary Button (Action) */
    div.stButton > button {
        background-color: #059669 !important; /* Emerald Green */
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #047857 !important; 
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONALITY ---
check_authentication()
render_navbar()

st.title("🧪 New Soil Analysis")

with st.form("test_form"):
    st.markdown("### Farm Details")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        area = st.number_input("Survey Area (Acres)", min_value=0.1, step=0.1)
    with col2:
        nutrient = st.selectbox("Primary Target Nutrient", ["Fe", "Zn", "Cu", "Mn","B","Mg","P","S"])
    
    st.write("") # Spacer
    
    if st.form_submit_button("Initialize Analysis ➔", use_container_width=True):
        # Save the core farm data to pass to the processing page
        st.session_state["current_test"] = {
            "area": area, 
            "nutrient": nutrient
        }
        st.switch_page("pages/Processing.py")