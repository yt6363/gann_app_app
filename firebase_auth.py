import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st
import os

@st.cache_resource
def init_firebase():
    key_path = "serviceAccountKey.json"
    if not os.path.exists(key_path):
        st.error("Firebase serviceAccountKey.json file not found. Please add it to your project root.")
        st.stop()
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

def verify_user(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        st.error("Error verifying token: " + str(e))
        return None
