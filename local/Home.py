import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Home")
st.write("Welcome to the Streamlit application! Below are the two main features:")

col1, col2 = st.columns(2)

card_style = """
    <style>
    .equal-height-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 320px;  /* You can adjust this value as needed */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.03);
    }
    </style>
"""
st.markdown(card_style, unsafe_allow_html=True)

with col1:
    with st.container():
        st.markdown("""
            <div class="equal-height-card" style="border: 2px solid #1f77b4;">
                <h3>📰 Daily News</h3>
                <p>📅 Automatically updates with the latest news every day.</p>
                <ul>
                    <li>Aggregated from reliable sources</li>
                    <li>Displayed in chronological order</li>
                    <li>Simple and easy-to-read interface</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("""
            <div class="equal-height-card" style="border: 2px solid #2ca02c;">
                <h3>🔍 Custom Search</h3>
                <p>🎯 Filter and search for news your way.</p>
                <ul>
                    <li>Enter keywords to find relevant news</li>
                    <li>Select date, category, source</li>
                    <li>Interactive interface</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
