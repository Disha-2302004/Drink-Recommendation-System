import streamlit as st
from lib.firebase_utils import get_auth_db
from firebase_admin import firestore as admin_fs

st.title("📝 Feedback")

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

auth, db = get_auth_db()
uid = st.session_state["user"]["localId"]

rating = st.slider("Rate the recommendations", 1, 5, 4)
comment = st.text_area("Tell us what we can improve")

if st.button("Submit"):
    try:
        db.collection("feedback").add({
            "user_id": uid,
            "rating": int(rating),
            "comment": comment,
            "ts": admin_fs.SERVER_TIMESTAMP
        })
        st.success("Thanks! Your feedback helps improve personalization.")
    except Exception as e:
        st.error(f"Could not save feedback: {e}")

st.divider()
st.subheader("ℹ️ What happens with your feedback?")
st.write("- It is stored in Firestore under the `feedback` collection.")
st.write("- You can later use it to refine your recommendation logic (e.g., weight positive ratings).")
