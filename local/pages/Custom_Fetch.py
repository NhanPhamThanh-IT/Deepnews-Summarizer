import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Custom Fetch", page_icon="🛠️", layout="wide")

def custom_fetch():
    st.header("Custom Fetch")
    st.write("This page allows you to scrape links from a specified URL.")

    st.subheader("Enter a URL")
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
    main()
