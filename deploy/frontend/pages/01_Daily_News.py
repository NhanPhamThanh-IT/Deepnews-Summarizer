import streamlit as st
from components.display import display_articles, display_article_content
from utils.api import fetch_articles

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

    # Liên kết đến trang Scrape Article
    st.markdown("[Scrape a specific CNN article by URL](#)", unsafe_allow_html=True, help="Go to the Scrape Article page")
    if st.button("Go to Scrape Article Page"):
        st.switch_page("pages/scrape_article.py")

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