import streamlit as st
import hashlib
import os
import csv
import pandas as pd
import uuid

# Configuration
DB_FILE = "users.csv"

def init_db():
    """Initialize the user database CSV if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Updated Schema to include user_name
            writer.writerow(["phone_number", "password_hash", "salt", "user_name"])

def hash_password(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().hex
    salted_password = password + salt
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed, salt

def verify_password(stored_hash, stored_salt, input_password):
    check_hash, _ = hash_password(input_password, stored_salt)
    return check_hash == stored_hash

def create_user(phone_number, password, user_name):
    """Validates uniqueness and saves the new user securely."""
    init_db()
    
    # --- DEFENSIVE CHECK ---
    try:
        df = pd.read_csv(DB_FILE, dtype={'phone_number': str})
        
        # If the old database schema is detected, raise an error to trigger the except block
        if 'phone_number' not in df.columns:
            raise KeyError("Old database schema detected.")
            
    except (FileNotFoundError, KeyError, pd.errors.EmptyDataError):
        # If the file is broken, old, or empty, wipe it and recreate the correct headers
        with open(DB_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["phone_number", "password_hash", "salt", "user_name"])
        df = pd.read_csv(DB_FILE, dtype={'phone_number': str})
    # ------------------------

    # Check if phone number already exists
    if str(phone_number) in df["phone_number"].values:
        return False, "An account with this phone number already exists."

    # Hash and Save
    hashed_pw, salt = hash_password(password)
    
    with open(DB_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([phone_number, hashed_pw, salt, user_name])
        
    return True, "Account created successfully."
def authenticate_user(phone_number, password):
    """Checks credentials and returns (Success_Bool, User_Name)."""
    init_db()
    
    try:
        # Read as string to prevent dropping leading zeros
        df = pd.read_csv(DB_FILE, dtype={'phone_number': str})
        user_record = df[df["phone_number"] == str(phone_number)]
        
        if user_record.empty:
            return False, None
        
        stored_hash = user_record.iloc[0]["password_hash"]
        stored_salt = user_record.iloc[0]["salt"]
        
        if verify_password(stored_hash, stored_salt, password):
            # Fetch the name from the database!
            fetched_name = user_record.iloc[0]["user_name"]
            return True, fetched_name
            
        return False, None
        
    except Exception as e:
        st.error(f"Authentication Error: {e}")
        return False, None

def check_authentication():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠️ Access Denied. Please log in.")
        st.switch_page("app.py")
        st.stop()

def logout_user():
    st.session_state.clear()
    st.switch_page("app.py")