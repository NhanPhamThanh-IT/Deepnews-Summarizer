import streamlit as st
import requests

API_BASE = "https://nlpapplication-0xrw.onrender.com"

def display_article_content(article_url):
    st.title("📄 Article Content")

    try:
        with st.spinner("Fetching article content..."):
            response = requests.get(f"{API_BASE}/scrape-article", params={"url": article_url}, timeout=100)
        if response.status_code == 200:
            content = response.json().get("content", "No content available.")
            st.markdown(content)
        else:
            st.error("Failed to fetch article content.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")

    # Back button
    if st.button("🔙 Back to articles"):
        st.session_state.selected_article_url = None
        st.rerun()

def display_articles(articles):
    for article in articles:
        with st.expander(f"### {article.get('title', 'No title')}"):
            article_url = article.get("url", "")
            if st.button("📖 Read more", key=article_url):
                st.session_state.selected_article_url = article_url
                st.rerun()
            st.markdown("---")

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

def main():
    st.title("📰 CNN News Scraper")
    st.write("This application uses FastAPI to scrape news from CNN.")

    # Khởi tạo session state
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

    # Tự động lấy bài viết khi tab được chọn
    fetch_articles(user_url)

    # Hiển thị danh sách bài viết nếu có
    if st.session_state.articles:
        display_articles(st.session_state.articles)

if __name__ == "__main__":
    main()