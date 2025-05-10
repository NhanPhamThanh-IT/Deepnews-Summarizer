import streamlit as st
import requests

def display_articles(articles):
    for article in articles:
        st.write(f"### {article['title']}")
        st.write(f"[Read more]({article['url']})")
        st.write("---")

def main():
    st.title("CNN News Scraper")
    st.write("This app scrapes the latest articles from CNN using an API.")

    # Gọi API từ FastAPI
    api_url = "http://127.0.0.1:8000/scrape"  # Đổi URL nếu cần
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        if articles:
            display_articles(articles)
        else:
            st.write("No articles found.")
    else:
        st.write("Error fetching data from the API.")

if __name__ == "__main__":
    main()
