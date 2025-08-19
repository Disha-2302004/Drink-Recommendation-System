# 🍹 Drink Recommender (Streamlit + Firebase)

This is a **3-page Netflix-style Streamlit app** with Firebase Authentication and Firestore persistence.

## Pages
1. **Login / Signup** (Firebase Email/Password)
2. **Personalized Recommendations** (TF-IDF similarity on your dataset)
3. **Feedback** (stores ratings/comments in Firestore)

---

## 🚀 Quick Start (Local)

1) Create a virtual env and install deps:
```bash
pip install -r requirements.txt
```

2) Create a local secrets file:
- Copy `.streamlit/secrets_template.toml` to `.streamlit/secrets.toml`
- Fill in your Firebase config and **service account** JSON values.

3) Put your dataset at: `cleaned_carbonated_drinks.csv`

4) Run the app:
```bash
streamlit run app.py
```

---

## 🌐 Deploy to Streamlit Cloud (streamlit.io)

1) Push this folder to a **GitHub repo** (ensure `app.py` is at repo root).
2) Go to **streamlit.io → New app → Connect your repo**.
3) **Main file path**: `app.py`
4) After deploy, open **App → Settings → Secrets** and paste the contents of your local `.streamlit/secrets.toml`.
5) Click **Save**. Your app will reload with Firebase connected.

> ⚠️ Never commit `serviceAccountKey.json`. Use **secrets** only.

---

## Dataset
- The app expects a CSV named `cleaned_carbonated_drinks.csv` in the project root.
- It uses columns like `Drink_Name`, `Flavor`, `Ingredients`, `Description` if present.

## Notes
- This starter uses **TF-IDF** to keep deployment fast & light.
- You can later switch to `sentence-transformers` + FAISS if needed.
