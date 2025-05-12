import streamlit as st
from components import set_page_config, display_heading

if __name__ == "__main__":
    set_page_config(page_title="Home", page_icon="🏠")

    display_heading(
        title="🏠 Home Page 🏠",
        description="Welcome to the Automated News Collector application — your intelligent companion for staying informed in the digital age. This application is designed to automatically gather, update, and summarize the latest news from a variety of trusted sources every single day. Thanks to its automated data collection system, you no longer need to spend time searching for news or checking multiple websites manually — all important content is compiled and presented in a clear, accessible, and user-friendly format. Whether you're interested in politics, technology, business, or entertainment, this app ensures that you stay up to date with timely and accurate information, helping you make better personal or professional decisions. All news is neatly organized to save you time while keeping you connected to the world around you."
    )

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
                    <h3 style='text-align: center;'>📰 Daily News</h3>
                    <p>Automatically updates with the latest news every day.</p>
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
                    <h3 style='text-align: center;'>🔍 Custom Search</h3>
                    <p>Easily filter and search the news that matters to you — anytime, your way.</p>
                    <ul>
                        <li>Enter keywords to find relevant news</li>
                        <li>Select date, category, source</li>
                        <li>Interactive interface</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
