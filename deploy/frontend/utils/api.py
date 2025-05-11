import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE = os.getenv("API_BASE", "https://nlpapplication.onrender.com")

def fetch_articles(user_url):
    if not user_url.startswith("https://edition.cnn.com"):
        st.warning("⚠️ Only CNN URLs (https://edition.cnn.com/...) are accepted.")
        return

    try:
        with st.spinner("Fetching data..."):
            response = requests.get(f"{API_BASE}/scrape", params={"url": user_url}, timeout=10)

        if response.status_code == 200:
            data = response.json()
            st.session_state.articles = data.get("articles", [])
            if not st.session_state.articles:
                st.info("No articles found.")
        else:
            st.error(f"API Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot connect to the API: {e}")