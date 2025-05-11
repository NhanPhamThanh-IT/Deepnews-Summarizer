import streamlit as st
import requests
from utils.api import API_BASE

def display_articles(articles):
    for article in articles:
        with st.expander(f"### {article.get('title', 'No title')}"):
            article_url = article.get("url", "")
            if st.button("📖 Read more", key=article_url):
                st.session_state.selected_article_url = article_url
                st.rerun()
            st.markdown("---")

def display_article_content(article_url):
    st.markdown(
        """
        <div style="text-align: center;">
            <h3>Article Content</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Custom CSS for adding a border
    st.markdown(
        """
        <style>
        .article-content {
            border: 2px solid #d3d3d3;
            border-radius: 8px;
            padding: 15px 25px;
            margin: 10px;
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    try:
        with st.spinner("Fetching article content..."):
            response = requests.get(f"{API_BASE}/scrape-article", params={"url": article_url}, timeout=100)
        if response.status_code == 200:
            content = response.json().get("content", "No content available.")
            # Wrap content in a div with the article-content class
            st.markdown(f'<div class="article-content">{content}</div>', unsafe_allow_html=True)
        else:
            st.error("Failed to fetch article content.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")