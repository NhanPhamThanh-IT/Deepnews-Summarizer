import streamlit as st

def set_page_config(page_title: str, page_icon: str) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide"
    )

def set_header(title: str, description: str) -> None:
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
