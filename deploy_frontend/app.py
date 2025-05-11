import streamlit as st
import requests

def display_articles(articles):
    for article in articles:
        st.markdown(f"### {article.get('title', 'No title')}")
        st.markdown(f"[Read more]({article.get('url', '#')})")
        st.markdown("---")

def main():
    st.title("📰 CNN News Scraper")
    st.write("Ứng dụng này dùng FastAPI để thu thập tin tức từ CNN.")

    # Nhập URL tùy chỉnh
    default_url = "https://edition.cnn.com/us"
    user_url = st.text_input("Nhập URL CNN muốn scrape:", value=default_url)

    if st.button("Lấy bài viết"):
        if not user_url.startswith("https://edition.cnn.com"):
            st.warning("⚠️ Chỉ chấp nhận URL từ CNN (https://edition.cnn.com/...)")
            return

        api_url = "https://nlpapplication.onrender.com/scrape"
        params = {"url": user_url}

        try:
            with st.spinner("Đang lấy dữ liệu..."):
                response = requests.get(api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                if articles:
                    display_articles(articles)
                else:
                    st.info("Không tìm thấy bài viết nào.")
            else:
                st.error(f"Lỗi từ API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Không thể kết nối tới API: {e}")

if __name__ == "__main__":
    main()
