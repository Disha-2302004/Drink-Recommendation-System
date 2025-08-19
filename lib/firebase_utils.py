import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def get_auth_db():
    try:
        # Firebase Web API config (used by pyrebase for Auth)
        fb_cfg = st.secrets["firebase"]["config"]

        # Firebase Service Account (used by firebase_admin for Firestore)
        svc = st.secrets["firebase"]["service_account"]
    except KeyError as e:
        st.error(f"❌ Missing Firebase secret: {e}. Please check Streamlit Cloud → Settings → Secrets.")
        st.stop()

    # Initialize pyrebase for Authentication
    firebase = pyrebase.initialize_app(dict(fb_cfg))
    auth = firebase.auth()

    # Initialize Firebase Admin SDK for Firestore (only once)
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(svc))
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    return auth, db
