import streamlit as st
import time

def render_navbar():
    # --- 1. CSS TO HIDE DEFAULT page LINKS ---
    st.markdown("""
    <style>
        /* Hides the automatic page navigation list in the sidebar */
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 2. CUSTOM SIDEBAR CONTENT ---
    with st.sidebar:
        # Project Name
        st.header("🌾 LISA") 
        #st.write("Smart Agriculture System")
        
        st.write("---") # Divider line
        
        # Logout Button
        if st.button("🔒 Logout", type="primary", use_container_width=True):
            st.session_state.clear()
            st.toast("Logging out...", icon="🔒")
            time.sleep(0.5)
            st.switch_page("app.py")