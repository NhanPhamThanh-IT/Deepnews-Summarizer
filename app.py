import streamlit as st

# Cấu hình trang chính
st.set_page_config(page_title="Multi-Page App", page_icon="🌐", layout="wide")

# Nội dung trang chính
st.title("Welcome to the Multi-Page App")
st.write("This is a multi-page Streamlit application with tools for web scraping and other tasks.")
st.markdown("""
Use the **sidebar** on the left to navigate between:
- **Scraper**: Extract links from a website using a URL and CSS selector.
- **Other Tasks**: Perform additional tasks like text input and simple calculations.
""")

# Sidebar điều hướng
st.sidebar.header("Navigation")
st.sidebar.write("Select a page to explore:")
# Các trang trong thư mục `pages/` sẽ tự động xuất hiện trong sidebar