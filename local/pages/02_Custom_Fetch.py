import streamlit as st
from utils import get_content_from_direct_url, load_config
from config import set_header, set_page_config, setup_asyncio_policy

DEFAULT_URL = "https://example.com"

try:
    CONFIG = load_config()
except FileNotFoundError:
    st.error("Error: Configuration file (config.yaml or similar) not found. Using default values.")
    CONFIG = {}
except Exception as e:
    st.error(f"Critical error while loading configuration: {e}. Using default values.")
    CONFIG = {}

def display_fetched_content(content):
    if not content:
        st.info("No content fetched.")
        return
    st.subheader("Fetched Content")
    with st.expander("Show content", expanded=True):
        st.markdown(content)

def fetch_content(url, results_area):
    if not url:
        results_area.error("Error: URL cannot be empty.")
        return

    results_area.info(f"Fetching content from: {url}...")
    try:
        with st.spinner(f"Connecting and analyzing {url}... Please wait."):
            content = get_content_from_direct_url(url)

        if content:
            results_area.success("Successfully retrieved data!")
            display_fetched_content(content)
        else:
            results_area.info("No content found.")

    except ConnectionError as ce:
        results_area.error(f"Connection error: {ce}")
    except ValueError as ve:
        results_area.error(f"Invalid input: {ve}")
    except Exception as e:
        results_area.error("An unexpected error occurred.")
        st.exception(e)

def main():
    # Initialize session state for URL input
    if 'url' not in st.session_state:
        st.session_state.url = CONFIG.get("url", DEFAULT_URL)

    # Create input field and fetch button
    st.text_input("Enter URL to fetch content:", 
                 value=st.session_state.url, 
                 key="url_input",
                 on_change=lambda: setattr(st.session_state, 'url', st.session_state.url_input))
    
    results_area = st.empty()
    
    if st.button("Fetch Content"):
        fetch_content(st.session_state.url, results_area)

if __name__ == "__main__":
    setup_asyncio_policy()
    set_page_config(
        page_title="Custom Fetch", 
        page_icon="🔍"
    )
    set_header(
        title="Custom Fetch",
        description="This page allows you to enter a URL and fetch data from it.",
    )
    main()