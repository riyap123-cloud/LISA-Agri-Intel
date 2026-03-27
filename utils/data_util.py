import streamlit as st
import pandas as pd
from datetime import datetime

def init_data():
    if "test_history" not in st.session_state:
        # Mock initial data - Added "Moisture" and changed "Farmer" to phone numbers
        st.session_state["test_history"] = [
            {"Date": "2023-10-01 10:00", "Phone": "9999999999", "Crop": "Wheat", "Nutrient": "Fe", "Value": 45, "Moisture": 38.5, "Result": "Low"},
            {"Date": "2023-10-05 14:30", "Phone": "8888888888", "Crop": "Corn", "Nutrient": "Zn", "Value": 65, "Moisture": 42.0, "Result": "Optimal"}
        ]

def save_test_result(data):
    if "test_history" not in st.session_state:
        init_data()
    
    # Grabbing the phone_number from session state
    user_phone = st.session_state.get("phone_number", "Unknown")
    
    record = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Phone": user_phone,
        "Crop": data.get("crop"),
        "Nutrient": data.get("nutrient"),
        "Value": data.get("value", 0), # Default to 0 if not provided
        "Moisture": data.get("moisture", 0.0), # The new moisture field!
        "Result": data.get("status", "Pending")
    }
    st.session_state["test_history"].append(record)

def get_all_history():
    if "test_history" not in st.session_state:
        init_data()
    return pd.DataFrame(st.session_state["test_history"])

def get_user_history(phone_number):
    df = get_all_history()
    # Filter by the exact phone number
    return df[df["Phone"] == phone_number]