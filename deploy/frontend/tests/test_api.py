import pytest
import requests
from unittest.mock import patch
from utils.api import fetch_articles
import streamlit as st

@pytest.fixture
def setup_session_state():
    st.session_state.articles = []

@patch("requests.get")
def test_fetch_articles_valid_url(mock_get, setup_session_state):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"articles": [{"title": "Test", "url": "https://edition.cnn.com/test"}]}
    
    fetch_articles("https://edition.cnn.com/politics")
    assert len(st.session_state.articles) == 1
    assert st.session_state.articles[0]["title"] == "Test"

@patch("requests.get")
def test_fetch_articles_invalid_url(mock_get, setup_session_state):
    fetch_articles("https://example.com")
    assert len(st.session_state.articles) == 0