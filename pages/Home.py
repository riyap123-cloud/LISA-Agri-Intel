import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# --- page CONFIG ---
st.set_page_config(page_title="Agri-Intel Dashboard", page_icon="🌾", layout="wide")

# FORCE PATH FIX
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth_utils import check_authentication
from components.navbar import render_navbar
from utils.data_util import get_user_history

# --- 🎨 ENTERPRISE SAAS UI DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"], [class*="st-"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #F8FAFC; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding-top: 2rem !important; max-width: 1200px; }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); padding: 24px; transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover { 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08); transform: translateY(-2px); 
    }
    
    h1, h2, h3 { color: #0F172A !important; letter-spacing: -0.02em; }
    p { color: #475569 !important; font-size: 1rem; line-height: 1.5; }
    
    div.stButton > button { 
        background-color: #059669 !important; color: white !important; border: none; 
        border-radius: 8px; font-weight: 600; padding: 0.5rem 1rem; transition: all 0.2s; 
    }
    div.stButton > button:hover { background-color: #047857 !important; }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) div.stButton > button { 
        background-color: #FFFFFF !important; color: #0F172A !important; border: 1px solid #CBD5E1 !important; 
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) div.stButton > button:hover { 
        background-color: #F1F5F9 !important; 
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONALITY ---
check_authentication()
render_navbar()

# Extracting data from Session State
display_name = st.session_state.get('user_name', 'Demo User')
user_phone = st.session_state.get('phone_number')
current_date = datetime.now().strftime("%A, %B %d, %Y")

# --- HEADER SECTION ---
st.markdown(f"<p style='margin-bottom: -15px; font-size: 0.9rem; font-weight: 600; color: #64748B !important;'>{current_date}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: 2.5rem;'>Welcome back, {display_name}</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-bottom: 2rem;'>Monitor your soil health and generate AI-driven insights below.</p>", unsafe_allow_html=True)

# --- MAIN ACTION CARDS ---
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>🧪 New Soil Analysis</h3>", unsafe_allow_html=True)
        st.write("Initiate a new diagnostic test. Our AI model will process current parameter values to recommend optimal crop choices.")
        st.write("") 
        if st.button("Initialize New Test ➔", use_container_width=True):
            st.switch_page("pages/Test.py")

with col2:
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0;'>📊 Historical Data</h3>", unsafe_allow_html=True)
        st.write("Access your securely stored historical diagnostic reports. Analyze temporal trends in your soil composition.")
        st.write("") 
        if st.button("View Analytics Hub", use_container_width=True):
            st.session_state["show_history"] = not st.session_state.get("show_history", False)

# --- DATA TABLE (HISTORY) ---
if st.session_state.get("show_history"):
    st.markdown("<hr style='border: 1px solid #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### Diagnostic History")
    
    with st.container(border=True):
        df = get_user_history(user_phone)
        if df is not None and not df.empty:
            display_df = df.drop(columns=['Phone']) if 'Phone' in df.columns else df
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No historical records located. Run your first analysis to populate this table.")