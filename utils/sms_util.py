# utils/sms_util.py
import streamlit as st
from twilio.rest import Client

def send_test_completion_sms(phone_number, crop, nutrient, status, kg_acre):
    """Sends an SMS alert to the farmer when a test is completed."""
    try:
        # Load credentials from secrets
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        twilio_number = st.secrets["TWILIO_PHONE_NUMBER"]

        client = Client(account_sid, auth_token)

        # Format the phone number (Twilio requires country codes, e.g., +91 for India)
        if not phone_number.startswith("+"):
            phone_number = "+91" + phone_number # Change +91 if you are in a different country

        # Create the message
        message_body = f"🌾 LISA Alert: Your soil test for {crop} ({nutrient}) is complete!\nResult: {kg_acre} kg/acre.\nStatus: {status}.\nPlease check your dashboard for the full AI report."

        # Send the SMS
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=phone_number
        )
        
        return True, message.sid

    except Exception as e:
        return False, str(e)