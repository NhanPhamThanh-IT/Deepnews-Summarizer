import streamlit as st
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="AI-Powered Web News Scraper & Summarizer",
    page_icon="📰",
    layout="wide"
)

# Hide Streamlit elements
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Read HTML content
html_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
with open(html_file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Display the HTML content
components.html(html_content, height=5000, scrolling=True)
