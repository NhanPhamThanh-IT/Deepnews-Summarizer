import streamlit as st
from utils import get_links_from_homepage, load_config
import asyncio
import sys

import asyncio
import sys

def setup_asyncio_policy(platform):
    """Set asyncio policy based on the platform."""
    try:
        # Windows: Ensure the correct event loop policy is set.
        loop = asyncio.get_event_loop()
        if not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except RuntimeError:
        # If there's no event loop yet, set the policy
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception as e:
        print(f"[Warning] Could not set Windows asyncio policy: {e}")

st.set_page_config(page_title="Daily News", page_icon="🔗", layout="wide")

try:
    CONFIG = load_config()
except FileNotFoundError:
    st.error("Error: Configuration file (config.yaml or similar) not found. Using default values.")
    CONFIG = {}
except Exception as e:
    st.error(f"Critical error while loading configuration: {e}. Using default values.")
    CONFIG = {}

DEFAULT_URL = "https://example.com"
DEFAULT_CSS_SELECTOR = "a"

def display_scraped_links(links_data):
    if not links_data:
        st.info("No links found.")
        return

    st.subheader("Hot News")
    with st.expander("Show all links", expanded=True):
        for index, link_info in enumerate(links_data):
            title = link_info.get('title', 'N/A')
            url = link_info.get('url', '#')
            st.markdown(f"{index + 1}. **{title.strip()}**: [{url.strip()}]({url.strip()})")

def scrape_links(url, css_selector, results_area):
    if not url:
        results_area.error("Error: URL cannot be empty.")
        return
    if not css_selector:
        results_area.error("Error: CSS Selector cannot be empty.")
        return

    results_area.info(f"Scraping links from: {url}...")
    try:
        with st.spinner(f"Connecting and analyzing {url}... Please wait."):
            links = get_links_from_homepage(url, css_selector)

        if links:
            results_area.success("Successfully retrieved data!")
            display_scraped_links(links)
        else:
            results_area.info("No links found or no elements match the CSS selector.")

    except ConnectionError as ce:
        results_area.error(f"Connection error: {ce}")
    except ValueError as ve:
        results_area.error(f"Invalid input: {ve}")
    except Exception as e:
        results_area.error("An unexpected error occurred.")
        st.exception(e)

def main():
    # Lấy URL và CSS selector từ config hoặc dùng mặc định
    url = CONFIG.get("url", DEFAULT_URL)
    css_selector = CONFIG.get("css_selector", DEFAULT_CSS_SELECTOR)

    results_area = st.empty()
    scrape_links(url, css_selector, results_area)

if __name__ == "__main__":
    # platform = sys.platform
    # setup_asyncio_policy(platform)
    main()
