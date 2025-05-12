import streamlit as st
from components.display import display_article_content
from components import set_page_config, display_heading

def is_valid_url(url):
    """Kiểm tra xem URL có hợp lệ hay không."""
    if not url.strip():
        return False
    if not url.startswith("https://"):
        return False
    return True

def main():
    article_url = st.text_input("Enter an article URL (e.g., https://example.com/):", "")

    if article_url.strip():
        if is_valid_url(article_url):
            if st.button("Scrape"):
                display_article_content(article_url)
        else:
            st.error("Please enter a valid URL starting with 'https://' (e.g., https://example.com/).")
    else:
        st.info("Enter an article URL to proceed.")

if __name__ == "__main__":
    set_page_config(
        page_title="Scrape Specific Article",
        page_icon="📄"
    )
    display_heading(
        title="📄 Scrape Specific Article",
        description="Please enter the URL of the news article you would like to extract. Once submitted, the application will automatically retrieve the content from the provided link, process it, and display the main text of the article for your review and further use."
    )
    main()