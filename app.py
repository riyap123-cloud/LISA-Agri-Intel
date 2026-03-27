import streamlit as st
from auth.user_login import show_user_login
from auth.user_signup import show_user_signup

# Configure page settings
st.set_page_config(page_title="LISA - Soil Assistant", page_icon="🌾", layout="centered")

# Initialize Session State
if "page" not in st.session_state:
    st.session_state["page"] = "splash"

# Check if logged in (Gatekeeper)
if st.session_state.get("logged_in"):
    st.switch_page("pages/Home.py")

else:
    # --- 🎨 ADDED: Background Color CSS & Hide Sidebar ---
    st.markdown("""
    <style>
        /* This completely hides the sidebar on Splash, Login, and Signup page */
        [data-testid="stSidebar"] { 
            display: none !important; 
        }
        .stApp {
            background: linear-gradient(to bottom, #A3FFEE, #dcedc8);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 🌾 LISA Splash Screen ---
    if st.session_state["page"] == "splash":
        
        # --- 🔴 RED BUTTON CSS (Only applies to Splash Screen) ---
        st.markdown("""
        <style>
            div.stButton > button {
                background: linear-gradient(90deg, #D32F2F 0%, #B71C1C 100%) !important; /* Red Gradient */
                color: white !important;
                border: 1px solid #B71C1C !important;
                border-radius: 8px !important;
                font-size: 18px !important;
                font-weight: bold !important;
                padding: 10px 0 !important;
                box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4) !important;
                transition: 0.3s !important;
            }
            div.stButton > button:hover {
                transform: scale(1.02) !important;
                box-shadow: 0 6px 20px rgba(183, 28, 28, 0.6) !important;
                background: #B71C1C !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Friendly Header
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌾 LISA 🌾</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #558b2f;'>At Your Service</h3>", unsafe_allow_html=True)
        
        st.write("---")
        
        # Welcoming Text
        st.markdown(
            """
            <div style='text-align: center; font-size: 1.1rem; color: #33691e;'>
                <b>Namaste!</b> I am your smart farm assistant.<br>
                I can help you test your soil nutrients and suggest the best fertilizers.<br><br>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Big Action Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("") # Spacer
            if st.button("🚜 Enter Farm Dashboard", type="primary", use_container_width=True):
                st.session_state["page"] = "user_auth"
                st.session_state["auth_mode"] = "login"
                st.rerun()

        st.write("")
        st.markdown("<div style='text-align: center; color:#4C9C9C; font-size: 0.8rem;'>Powered by IoT Technology</div>", unsafe_allow_html=True)

    # --- User Auth (Login / Signup) ---
    elif st.session_state["page"] == "user_auth":
        
        auth_mode = st.session_state.get("auth_mode", "login")
        
        if auth_mode == "login":
            show_user_login()
            
            # Switch to Signup (DARK, BOLD TEXT)
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            st.markdown("<span style='color: #1a1a1a; font-weight: 700; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>Don't have an account?</span>", unsafe_allow_html=True)
            if st.button("Create New Account"):
                st.session_state["auth_mode"] = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            show_user_signup()
            
            # Switch to Login (DARK, BOLD TEXT)
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            st.markdown("<span style='color: #1a1a1a; font-weight: 700; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>Already have an account?</span>", unsafe_allow_html=True)
            if st.button("Back to Login"):
                st.session_state["auth_mode"] = "login"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)