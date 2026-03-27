import requests
import streamlit as st
import time

# Base URL for ThingSpeak
THINGSPEAK_UPDATE_URL = "https://api.thingspeak.com/update"

# ==========================================
# 1. GENERIC FUNCTIONS (For Result.py)
# ==========================================

def send_to_thingspeak(write_api_key, field1_val, field2_val, field3_val):
    """
    Uploads a finished result to the cloud.
    Used in Result.py
    """
    payload = {
        "api_key": write_api_key,
        "field1": field1_val,  
        "field2": field2_val,  
        "field3": field3_val   
    }
    
    try:
        response = requests.get(THINGSPEAK_UPDATE_URL, params=payload)
        if response.status_code == 200 and response.text != "0":
            return True, f"Data Sent! (Entry ID: {response.text})"
        else:
            return False, "Failed. Check API Key."
    except Exception as e:
        return False, f"Connection Error: {e}"

def get_latest_thingspeak_data(channel_id, read_api_key):
    """
    Fetches the latest data.
    Used in Result.py
    """
    try:
        url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_api_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# ==========================================
# 2. IOT TRIGGER FUNCTIONS (For Processing.py)
# ==========================================

def trigger_esp32_scan(write_api_key, command_code):
    """
    Sends command '1' or '2' to Field 8 to wake up ESP32.
    Used in Processing.py
    """
    payload = {
        "api_key": write_api_key,
        "field8": command_code
    }
    try:
        requests.get(THINGSPEAK_UPDATE_URL, params=payload)
        return True
    except:
        return False

def wait_for_sensor_data(channel_id, read_api_key):
    """
    Loops and waits for Field 8 to return to '0'.
    Used in Processing.py
    """
    progress_text = "Waiting for Sensor..."
    my_bar = st.progress(0, text=progress_text)

    # Poll for 45 seconds
    for i in range(45):
        # Update UI
        percent = min(i * 2, 95)
        my_bar.progress(percent, text=f"Waiting for ESP32... ({i}s)")
        
        try:
            # Check Cloud
            data = get_latest_thingspeak_data(channel_id, read_api_key)
            
            if data:
                # Check Command Flag (Field 8)
                # ESP32 sets this to '0' when it uploads data
                flag = int(data.get("field8", -1))
                
                if flag == 0:
                    my_bar.progress(100, text="Data Received!")
                    time.sleep(0.5)
                    my_bar.empty()
                    return data
        except:
            pass
        
        time.sleep(1) # Wait 1 sec before next check

    my_bar.empty()
    st.error("Timeout: ESP32 did not respond.")
    return None