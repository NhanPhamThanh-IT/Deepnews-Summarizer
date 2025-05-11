import pytest
from unittest.mock import patch
import streamlit as st
from components.display import display_articles, display_article_content

@pytest.fixture
def setup_session_state():
    st.session_state.selected_article_url = None

@patch("streamlit.button")
def test_display_articles(mock_button, setup_session_state):
    articles = [{"title": "Test Article", "url": "https://edition.cnn.com/test"}]
    mock_button.return_value = True
    
    with patch("streamlit.session_state", {"selected_article_url": None}):
        display_articles(articles)
        assert st.session_state.selected_article_url == "https://edition.cnn.com/test"

@patch("requests.get")
def test_display_article_content(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"content": "Test content"}
    
    with patch("streamlit.markdown") as mock_markdown:
        display_article_content("https://edition.cnn.com/test")
        mock_markdown.assert_called_with("Test content")