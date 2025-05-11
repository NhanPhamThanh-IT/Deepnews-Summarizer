import streamlit as st
from utils import get_links_from_homepage, load_config
import asyncio
import asyncio
import sys

def setup_asyncio_policy():
    """Set asyncio policy based on the current platform."""
    platform = sys.platform

    if platform.startswith('win'):
        try:
            # Import WindowsProactorEventLoopPolicy only if on Windows
            from asyncio import WindowsProactorEventLoopPolicy

            if not isinstance(asyncio.get_event_loop_policy(), WindowsProactorEventLoopPolicy):
                asyncio.set_event_loop_policy(WindowsProactorEventLoopPolicy())
        except (RuntimeError, ImportError, AttributeError) as e:
            print(f"[Warning] Could not set Windows asyncio policy: {e}")

    elif platform.startswith('linux'):
        try:
            try:
                import uvloop
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                print("Running on Linux platform with UVLoop policy for enhanced performance.")
            except ImportError:
                print("Running on Linux platform. Using default asyncio event loop (uvloop not installed).")

            try:
                import resource
                soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
                if soft_limit < 1024:
                    resource.setrlimit(resource.RLIMIT_NOFILE, (1024, hard_limit))
                    print("Increased file descriptor limit for better performance.")
            except (ImportError, ValueError, resource.error) as e:
                print(f"[Warning] Could not adjust file descriptor limit: {e}")

        except Exception as e:
            print(f"[Warning] Error setting up Linux asyncio configuration: {e}")

    else:
        print(f"[Info] Unknown or unsupported platform: {platform}. No special handling applied.")

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
    setup_asyncio_policy()
    main()