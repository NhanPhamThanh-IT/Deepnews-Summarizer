import streamlit as st
from utils import setup_asyncio_policy_if_windows, get_links_from_homepage, load_config
from ui import display_page_configuration

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
    url_input = st.sidebar.text_input(
        label="Website URL:",
        value=CONFIG.get("url", DEFAULT_URL),
        placeholder="https://www.example.com",
        help="Enter the full URL of the page you want to scrape data from (e.g., https://example.com)."
    )
    selector_input = st.sidebar.text_input(
        label="CSS Selector:",
        value=CONFIG.get("css_selector", DEFAULT_CSS_SELECTOR),
        placeholder="e.g., 'article.post > h2 > a'",
        help="Enter the CSS selector to find the elements containing links (e.g., 'a', '.my-class > a')."
    )
    return url_input, selector_input

def display_scraped_links(links_data):
    if not links_data:
        st.info("No links data to display.")
        return

    st.subheader("Scraped Links:")
    with st.expander("See all links", expanded=True):
        for index, link_info in enumerate(links_data):
            title = link_info.get('title', 'N/A')
            url = link_info.get('url', '#')
            st.markdown(f"{index + 1}. **{title.strip()}**: [{url.strip()}]({url.strip()})")

def main():
    display_page_configuration()
    current_url, current_css_selector = display_input_controls()

    if st.sidebar.button("Start Scraping Links", type="primary", use_container_width=True):
        if not current_url:
            st.error("Error: URL cannot be empty. Please enter a URL.")
            return
        if not current_css_selector:
            st.error("Error: CSS Selector cannot be empty. Please enter a CSS Selector.")
            return

        results_area = st.empty()
        results_area.info(f"Scraping links from: {current_url}...")

        try:
            with st.spinner(f"Connecting and analyzing {current_url}... Please wait a moment."):
                links = get_links_from_homepage(current_url, current_css_selector)

            if links:
                results_area.success("Data scraped successfully!")
                display_scraped_links(links)
            else:
                results_area.info("No links found on the page or no links matching your CSS selector.")

        except ConnectionError as ce:
             results_area.error(f"Connection error: Could not connect to {current_url}. Please check the URL and your network connection. Details: {ce}")
        except ValueError as ve:
            results_area.error(f"Input data error: {ve}")
        except Exception as e:
            results_area.error(f"An unexpected error occurred during data scraping.")
            st.exception(e)

if __name__ == "__main__":
    if setup_asyncio_policy_if_windows() != None:
        st.warning("Windows Proactor Event Loop Policy set successfully.")
    main()
