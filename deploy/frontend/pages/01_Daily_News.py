import streamlit as st
from components.display import display_articles, display_article_content
from utils.api import fetch_articles
from components import display_heading

def main():
    if "selected_article_url" not in st.session_state:
        st.session_state.selected_article_url = None
    if "articles" not in st.session_state:
        st.session_state.articles = []
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = "Politics"

    # Nếu đang xem nội dung bài viết
    if st.session_state.selected_article_url:
        display_article_content(st.session_state.selected_article_url)
        return

    tabs = ["Politics", "Sports", "Science", "Travel", "Health"]
    selected_tab = st.radio("Select a tab:", tabs, index=tabs.index(st.session_state.selected_tab), horizontal=True)

    if selected_tab != st.session_state.selected_tab:
        st.session_state.selected_tab = selected_tab
        st.session_state.articles = []

    tab_urls = {
        "Science": "https://edition.cnn.com/science",
        "Travel": "https://edition.cnn.com/travel",
        "Health": "https://edition.cnn.com/health",
        "Politics": "https://edition.cnn.com/politics",
        "Sports": "https://edition.cnn.com/sport"
    }

    user_url = tab_urls[st.session_state.selected_tab]
    st.write(f"Scraping news from: {user_url}")

    fetch_articles(user_url)

    if st.session_state.articles:
        display_articles(st.session_state.articles)

if __name__ == "__main__":
    display_heading(
        "📰 Automated News Collector",
        "With its fully automated daily update system, this platform continuously gathers the latest headlines and breaking news from trusted media outlets, ensuring that users are always presented with up-to-date, accurate, and relevant information—anytime, anywhere—without the need for manual intervention."
    )
    main()