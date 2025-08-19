import streamlit as st
from firebase_utils import init_firebase

db = init_firebase()  # now you can use Firestore


st.set_page_config(page_title="Drink Recommender", page_icon="🥤", layout="wide")

st.title("🥤 Netflix‑style Drink Recommender")
st.sidebar.success("Use the sidebar to open a page")

st.markdown(
    '''
Welcome! This app lets you:
- **Login/Signup** (Firebase Auth)
- Get **personalized drink recommendations**
- Leave **feedback** that is stored in Firestore

**How it remembers you:** We store your history and feedback in Firebase so your recos improve over time.
'''
)
