import streamlit as st

def display_page_configuration():
    """
    Configure the Streamlit page and display a styled title and caption.

    Description:
    -----------
    This function sets up the visual and layout configuration for a Streamlit web application
    named "Professional Web Scraper". It also renders the main page title and a short caption
    describing the purpose of the app.

    Behavior:
    --------
    - Sets the page title in the browser tab to "Professional Web Scraper".
    - Uses an empty page icon (can be replaced with an emoji or image URL if desired).
    - Expands the sidebar by default and uses a wide layout for better space usage.
    - Displays the main title of the app at the top of the page.
    - Adds a caption below the title with a brief description.

    Example:
    --------
    >>> display_page_configuration()
    # Browser tab title: "Professional Web Scraper"
    # Main page title: "Professional Web Scraper"
    # Caption: "A simple tool for extracting links from web pages."
    """
    st.set_page_config(
        page_title="Professional Web Scraper",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("Professional Web Scraper")
    st.caption("A simple tool for extracting links from web pages.")
