import streamlit as st
from utils import setup_asyncio_policy_if_windows, get_links_from_homepage, load_config
from ui import display_page_configuration

# Cấu hình trang
st.set_page_config(page_title="Link Scraper", page_icon="🔗", layout="wide")

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

def display_input_controls():
    st.sidebar.header("Scraper Configuration")
    if 'url' not in st.session_state:
        st.session_state.url = CONFIG.get("url", DEFAULT_URL)
    if 'css_selector' not in st.session_state:
        st.session_state.css_selector = CONFIG.get("css_selector", DEFAULT_CSS_SELECTOR)

    url_input = st.sidebar.text_input(
        label="Website URL:",
        value=st.session_state.url,
        placeholder="https://www.example.com",
        help="Enter the full URL of the page you want to scrape data from (e.g., https://example.com).",
        key="url_input"
    )
    selector_input = st.sidebar.text_input(
        label="CSS Selector:",
        value=st.session_state.css_selector,
        placeholder="e.g., 'article.post > h2 > a'",
        help="Enter the CSS selector to find the elements containing links (e.g., 'a', '.my-class > a').",
        key="selector_input"
    )
    st.session_state.url = url_input
    st.session_state.css_selector = selector_input
    # Lưu URL để chia sẻ với các trang khác
    st.session_state.shared_url = url_input
    return url_input, selector_input

def display_scraped_links(links_data):
    if not links_data:
        st.info("No links found.")
        return

    st.subheader("Scraped Links:")
    with st.expander("Show all links", expanded=True):
        for index, link_info in enumerate(links_data):
            title = link_info.get('title', 'N/A')
            url = link_info.get('url', '#')
            st.markdown(f"{index + 1}. **{title.strip()}**: [{url.strip()}]({url.strip()})")

def scrape_links(url, css_selector, results_area):
    if not url:
        results_area.error("Error: URL cannot be empty. Please enter a URL.")
        return
    if not css_selector:
        results_area.error("Error: CSS Selector cannot be empty. Please enter a CSS Selector.")
        return

    results_area.info(f"Scraping links from: {url}...")
    try:
        with st.spinner(f"Connecting and analyzing {url}... Please wait."):
            links = get_links_from_homepage(url, css_selector)

        if links:
            results_area.success("Successfully retrieved data!")
            display_scraped_links(links)
        else:
            results_area.info("No links found on the page or no elements match the CSS selector.")

    except ConnectionError as ce:
        results_area.error(f"Connection error: Could not connect to {url}. Please check the URL and your network. Details: {ce}")
    except ValueError as ve:
        results_area.error(f"Invalid input: {ve}")
    except Exception as e:
        results_area.error("An unexpected error occurred while scraping data.")
        st.exception(e)

def main():
    st.header("Link Scraper")
    st.write("Extract links from a website by providing a URL and a CSS selector.")
    current_url, current_css_selector = display_input_controls()
    results_area = st.empty()

    if 'scrape_triggered' not in st.session_state:
        st.session_state.scrape_triggered = False

    if st.sidebar.button("Start Scraping", type="primary", use_container_width=True, key="scrape_button"):
        results_area.empty()
        st.session_state.scrape_triggered = True
        scrape_links(current_url, current_css_selector, results_area)

    elif (
        not st.session_state.scrape_triggered and
        st.session_state.url and st.session_state.css_selector
    ):
        scrape_links(st.session_state.url, st.session_state.css_selector, results_area)

if __name__ == "__main__":
    if setup_asyncio_policy_if_windows() is not None:
        st.warning("Windows Proactor Event Loop Policy set successfully.")
    main()