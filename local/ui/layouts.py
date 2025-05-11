import streamlit as st

def display_page_configuration():
    st.set_page_config(
        page_title="Professional Web Scraper",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("Professional Web Scraper")
    st.caption("A simple tool for extracting links from web pages.")