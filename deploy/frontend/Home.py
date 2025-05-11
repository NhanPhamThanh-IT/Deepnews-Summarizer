import streamlit as st

if __name__ == "__main__":
    st.set_page_config(page_title="Home", page_icon="🏠")

    st.title("🏠 Home")
    st.write("Welcome to the Streamlit application! Below are the two main features:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📰 Daily News")
        st.write("📅 Automatically updates with the latest news every day.")
        st.markdown("""
        **Features:**
        - Aggregated from reliable sources
        - Displayed in chronological order
        - Simple and easy-to-read interface
        """)
        if st.button("🔎 Go to Daily News"):
            st.switch_page("pages/01_Daily_News.py")

    with col2:
        st.subheader("🔍 Custom Search")
        st.write("🎯 Filter and search for news your way.")
        st.markdown("""
        **Features:**
        - Enter keywords to find relevant news
        - Select date, category, source
        - Interactive interface
        """)
        if st.button("🔧 Go to Custom Search"):
            st.switch_page("pages/02_Custom_Fetch.py")
