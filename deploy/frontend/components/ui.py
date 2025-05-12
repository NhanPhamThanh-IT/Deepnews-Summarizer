import streamlit as st

def set_page_config(page_title: str, page_icon: str) -> None:
    """
    Set the page configuration for the Streamlit app.
    
    Args:
        page_title (str): The title of the page.
        page_icon (str): The icon to display in the browser tab.
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide"
    )

def display_heading(title: str, description: str) -> None:
    """
    Display a heading with a title and description.

    Args:
        title (str): The title to display.
        description (str): The description to display.
    """
    st.markdown(
        f"""
            <h1 style='text-align: center; color: #00ffff;'>{title}</h1>
            <p style='text-align: justify; color: #cccccc;'>{description}</p>
            <div style='margin-bottom: 50px;'></div>
        """,
        unsafe_allow_html=True
    )
