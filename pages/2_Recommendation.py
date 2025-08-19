import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from lib.firebase_utils import get_auth_db
from firebase_admin import firestore as admin_fs

st.title("🥤 Personalized Recommendations")

if "user" not in st.session_state:
    st.warning("Please login first on the Login/Signup page.")
    st.stop()

auth, db = get_auth_db()
uid = st.session_state["user"]["localId"]

@st.cache_data
def load_data_and_vectors(csv_path: str = "cleaned_carbonated_drinks.csv"):
    df = pd.read_csv(csv_path).fillna("")
    name_col = "Drink_Name" if "Drink_Name" in df.columns else df.columns[0]
    flavor = df["Flavor"] if "Flavor" in df.columns else ""
    ingr = df["Ingredients"] if "Ingredients" in df.columns else ""
    desc = df["Description"] if "Description" in df.columns else ""
    corpus = (flavor.astype(str) + " " + ingr.astype(str) + " " + desc.astype(str)).values

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return df, name_col, vectorizer, matrix

df, name_col, vectorizer, matrix = load_data_and_vectors()

st.subheader("Tell us what you feel like")
query = st.text_input("e.g., low sugar ginger caffeine‑free")

k = st.slider("How many suggestions?", 3, 20, 6)

def recommend(query: str, top_k: int = 6):
    qvec = vectorizer.transform([query])
    scores = cosine_similarity(qvec, matrix).flatten()
    top_idx = scores.argsort()[-top_k:][::-1]
    res = df.iloc[top_idx].copy()
    res["score"] = scores[top_idx]
    return res

if st.button("Get Recommendations") and query.strip():
    results = recommend(query, top_k=k)
    st.write("### 🔎 Recommendations for you")
    for _, row in results.iterrows():
        st.markdown(f"**{row.get(name_col, 'Drink')}**")
        st.caption(f"Flavor: {row.get('Flavor', '—')}")
        st.caption(f"Ingredients: {row.get('Ingredients', '—')}")
        st.progress(float(min(max(row['score'], 0.0), 1.0)))

    # Save to user history in Firestore
    try:
        db.collection("users").document(uid).set({
            "history": admin_fs.ArrayUnion([{
                "query": query,
                "top": results[[name_col, "Flavor", "Ingredients"]].to_dict(orient="records"),
                "ts": admin_fs.SERVER_TIMESTAMP
            }])
        }, merge=True)
    except Exception as e:
        st.warning(f"Could not save history: {e}")

# Show past history
st.divider()
st.subheader("📜 Your past queries")
try:
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        hist = (doc.to_dict() or {}).get("history", [])
        if hist:
            for h in reversed(hist[-10:]):
                st.write(f"**Query:** {h.get('query','')}")
                if h.get('top'):
                    for it in h['top'][:3]:
                        st.caption(f" • {it.get(name_col, 'Drink')}: {it.get('Flavor','')}")
                st.write("---")
        else:
            st.info("No history yet – get some recommendations!")
    else:
        st.info("User profile not found.")
except Exception as e:
    st.warning(f"Could not load history: {e}")
