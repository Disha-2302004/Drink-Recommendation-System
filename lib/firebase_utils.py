import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def get_auth_db():
    # Read secrets from .streamlit/secrets.toml (locally) or Streamlit Cloud Secrets
    fb_cfg = st.secrets["firebase"]["config"]
    svc = st.secrets["firebase"]["service_account"]

    firebase = pyrebase.initialize_app(fb_cfg)
    auth = firebase.auth()

    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(svc))  # accepts dict
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    return auth, db
