import streamlit as st
from config import set_header

def custom_fetch():
    url_input = st.text_input("Paste a URL here:", key="url_input", placeholder="https://example.com")
    if st.button("Submit URL", key="submit_url_button"):
        if url_input:
            st.session_state.shared_url = url_input
            st.success("URL submitted successfully!")
        else:
            st.warning("Please enter a URL before submitting.")

    if 'shared_url' in st.session_state:
        st.markdown(f"**URL from Scraper or Input**: {st.session_state.shared_url}")

def main():
    custom_fetch()

if __name__ == "__main__":
    set_header(
        title="Custom Fetch",
        description="This page allows you to enter a URL and fetch data from it.",
    )
    main()
