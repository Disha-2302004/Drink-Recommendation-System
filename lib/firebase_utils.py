import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_firebase():
    # Access firebase config
    firebase_config = st.secrets["firebase"]

    # Access service account
    service_account = st.secrets["firebase"]["service_account"]

    # Initialize Firebase only once
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(service_account))
        firebase_admin.initialize_app(cred, {
            "storageBucket": firebase_config["storageBucket"]
        })

    # Return Firestore client
    return firestore.client()
