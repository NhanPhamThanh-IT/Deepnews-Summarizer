import streamlit as st
from utils import get_links_from_homepage, load_config, get_content_from_direct_url
from config import set_header, set_page_config, setup_asyncio_policy

try:
    CONFIG = load_config()
except FileNotFoundError:
    st.error("Error: Configuration file (config.yaml or similar) not found. Using default values.")
    CONFIG = {}
except Exception as e:
    st.error(f"Critical error while loading configuration: {e}. Using default values.")
    CONFIG = {}

def display_scraped_links(links_data):
    if not links_data:
        st.info("No links found.")
        return
    
    st.subheader("Hot News")
    with st.expander("Show all links", expanded=True):
        for index, link_info in enumerate(links_data):
            title = link_info.get('title', 'N/A').strip()
            url = link_info.get('url', '#').strip()
            
            # Hiển thị tiêu đề và URL
            st.markdown(f"{index + 1}. **{title}**")
            
            # Tạo button và xử lý sự kiện click
            button_key = f"process_{index}_{url}"  # Key duy nhất cho mỗi button
            if st.button("More details", key=button_key):
                with st.spinner("Processing..."):
                    try:
                        result = get_content_from_direct_url(url)  # Gọi hàm xử lý từ file khác
                        st.markdown(
                            f"<div style='text-align: justify'>{result}</div>",
                            unsafe_allow_html=True
                        )

                    except Exception as e:
                        st.error(f"Error processing link: {str(e)}")

def scrape_links(url, css_selector, results_area, tab_name):
    if f"links_{tab_name}" not in st.session_state:
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
                st.session_state[f"links_{tab_name}"] = links

        except ConnectionError as ce:
            results_area.error(f"Connection error: {ce}")
            return
        except ValueError as ve:
            results_area.error(f"Invalid input: {ve}")
            return
        except Exception as e:
            results_area.error("An unexpected error occurred.")
            st.exception(e)
            return

    # Display cached links
    links = st.session_state.get(f"links_{tab_name}", [])
    if links:
        results_area.success("Successfully retrieved data!")
        display_scraped_links(links)
    else:
        results_area.info("No links found or no elements match the CSS selector.")

def main():
    TABS_CONFIG = CONFIG.get("tabs", [{
        "name": "Politics",
        "url": "https://edition.cnn.com/politics",
        "css_selector": ".container__link--type-article"
    },])

    # Create horizontal tabs based on TABS_CONFIG
    tab_names = [tab["name"] for tab in TABS_CONFIG]
    tabs = st.tabs(tab_names)

    # Iterate through tabs and their configurations
    for tab, config in zip(tabs, TABS_CONFIG):
        with tab:
            results_area = st.empty()
            scrape_links(
                url=config["url"],
                css_selector=config["css_selector"],
                results_area=results_area,
                tab_name=config["name"]
            )

if __name__ == "__main__":
    set_page_config(
        page_title="Daily News",
        page_icon="📰"
    )
    set_header(
        title="Daily News",
        description="This is a simple web scraping application that retrieves links from specified URLs using CSS selectors."
    )
    setup_asyncio_policy()
    main()