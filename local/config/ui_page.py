import streamlit as st

def set_page_config(page_title: str, page_icon: str) -> None:
    """
    Configure the basic settings for the Streamlit page.

    Parameters:
    ----------
    page_title : str
        The title that will be displayed in the browser tab.
    page_icon : str
        The icon (emoji or URL to an image) shown in the browser tab.

    Behavior:
    --------
    - Sets the page layout to 'wide' for better use of screen space.
    - Applies the given title and icon to the page.

    Example:
    --------
    >>> set_page_config("Dashboard", "📊")
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide"
    )

def set_header(title: str, description: str) -> None:
    """
    Render a custom-styled header at the top of the Streamlit app.

    Parameters:
    ----------
    title : str
        The main title to display, centered and styled with a green color.
    description : str
        A short paragraph describing the app or section, styled and justified for better readability.

    Behavior:
    --------
    - Displays the title in a centered, green-colored <h1> tag.
    - Shows the description below the title in a styled <p> tag.
    - Adds spacing below the header with a line break.

    Example:
    --------
    >>> set_header("Welcome to the App", "This app helps you visualize and explore data.")
    """
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <h1 style='color: #4CAF50;'>{title}</h1>
        </div>
        <div style='text-align: justify;'>
            <p style='font-size: 18px; color: #555;'>{description}</p>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
