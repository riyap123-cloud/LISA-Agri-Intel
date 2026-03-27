import streamlit as st
import sys
import os

# Fix path to see 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth_utils import authenticate_user

def show_user_login():
    # --- 🎨 FINAL CLEAN DESIGN (WIDER) ---
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1920&auto=format&fit=crop');
            background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;
        }
        
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); padding: 40px;
        }
        
        h2 { color: #FFFFFF !important; font-family: sans-serif; font-weight: 700; font-size: 2.5rem !important; margin-bottom: 0px !important; }
        p { color: #E0E0E0 !important; font-size: 1rem; margin-top: -5px; }
        label { color: #FFFFFF !important; font-weight: 500 !important; }
        
        /* 📝 INPUT FIELDS - Solid white for black text contrast */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.85) !important; 
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 8px; padding: 5px;
        }
        
        /* 🖤 BLACK TYPING TEXT */
        input[type="text"], input[type="password"] { 
            color: #000000 !important; 
            font-weight: 600 !important; 
        }
        
        /* 🌚 DARK GRAY PLACEHOLDER */
        ::placeholder { color: #666666 !important; opacity: 0.9; }
        
        /* 🔴 RED BUTTON COLORS */
        div.stButton > button {
            background: linear-gradient(90deg, #D32F2F 0%, #B71C1C 100%) !important; /* Red Gradient */
            color: white !important;
            border: 1px solid #B71C1C !important;
            border-radius: 8px; font-size: 18px; font-weight: bold; padding: 12px 0; width: 100%; margin-top: 10px; 
            box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4); transition: 0.3s;
        }
        
        div.stButton > button:hover { 
            transform: scale(1.01); 
            background: #B71C1C !important; /* Solid Darker Red on Hover */
            box-shadow: 0 6px 20px rgba(183, 28, 28, 0.6); 
        }
        
        .block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; }
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # --- 🟢 UI STRUCTURE (WIDER) ---
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: left;'>Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: left; margin-bottom: 25px;'>Welcome back! Please login to your account</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                phone_number = st.text_input("Phone Number", placeholder="Enter 10-digit mobile number")
                password = st.text_input("Password", type="password", placeholder="Password")
                st.checkbox("Remember me", value=True)
                st.write("") 
                submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
        # --- FUNCTIONALITY ---
        if submit:
            if not phone_number or not password:
                st.error("⚠️ Please enter both your phone number and password.")
            elif not phone_number.isdigit() or len(phone_number) != 10:
                st.error("⚠️ Please enter a valid 10-digit phone number.")
            else:
                success, fetched_name = authenticate_user(phone_number, password)
                
                if success:
                    st.toast("Login Successful!")
                    st.session_state["logged_in"] = True
                    st.session_state["phone_number"] = phone_number
                    st.session_state["user_name"] = fetched_name
                    st.session_state["role"] = "user"
                    st.switch_page("pages/Home.py")
                else:
                    st.error("Invalid Credentials. Please check your details and try again.")