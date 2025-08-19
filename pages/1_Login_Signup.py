import streamlit as st
from lib.firebase_utils import get_auth_db

st.title("🔐 Login / Signup")

auth, db = get_auth_db()

tab_login, tab_signup = st.tabs(["Login", "Signup"])

with tab_signup:
    email = st.text_input("Email (Signup)", key="signup_email")
    password = st.text_input("Password (Signup)", type="password", key="signup_pwd")
    username = st.text_input("Username", key="signup_user")
    if st.button("Create account"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            db.collection("users").document(uid).set({
                "username": username,
                "email": email,
                "history": [],
                "created_at": firestore.SERVER_TIMESTAMP
            })
            st.success("Account created! Please switch to Login.")
        except Exception as e:
            st.error(f"Signup error: {e}")

with tab_login:
    email_l = st.text_input("Email (Login)", key="login_email")
    password_l = st.text_input("Password (Login)", type="password", key="login_pwd")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email_l, password_l)
            st.session_state["user"] = user  # store token + localId
            st.success("Logged in! Go to the Recommendation page.")
        except Exception as e:
            st.error(f"Login error: {e}")

if "user" in st.session_state:
    if st.button("Log out"):
        del st.session_state["user"]
        st.info("Logged out.")
