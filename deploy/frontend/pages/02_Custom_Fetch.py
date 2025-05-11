import streamlit as st
from components.display import display_article_content

def is_valid_url(url):
    """Kiểm tra xem URL có hợp lệ hay không."""
    if not url.strip():
        return False
    if not url.startswith("https://"):
        return False
    # Kiểm tra thêm các điều kiện khác nếu cần (ví dụ: ký tự hợp lệ, domain, v.v.)
    return True

def main():
    st.title("📄 Scrape Specific Article")

    # Trường nhập URL bài báo
    article_url = st.text_input("Enter an article URL (e.g., https://example.com/):", "")

    # Kiểm tra tính hợp lệ của URL
    if article_url.strip():  # Chỉ kiểm tra nếu người dùng đã nhập gì đó
        if is_valid_url(article_url):
            if st.button("Scrape"):
                display_article_content(article_url)
        else:
            st.error("Please enter a valid URL starting with 'https://' (e.g., https://example.com/).")
    else:
        st.info("Enter an article URL to proceed.")

if __name__ == "__main__":
    main()