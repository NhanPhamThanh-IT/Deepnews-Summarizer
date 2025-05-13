# Automated News Web Scraper and Summarizer

## Overview

This project is a web application designed to automatically scrape news articles from web pages, summarize their content, and present them to the user. It features both a local development version with more direct control over scraping and summarization models, and a deployed version with a FastAPI backend and a Streamlit frontend.

## Features

*   **Automated News Scraping**: Fetches news articles from specified URLs.
    *   Local version uses `Crawl4AI` for flexible scraping.
    *   Deployed backend targets CNN news and uses `httpx` and `BeautifulSoup`.
*   **Content Summarization**:
    *   Local version utilizes a fine-tuned BART model (`HTThuanHcmus/bart-large-finetune-nlp`) for summarization.
    *   Deployed backend uses OpenAI's GPT-3.5-turbo for summarization.
*   **User Interface**:
    *   **Local**: Streamlit application ([`local/Home.py`](local/Home.py)) with pages for daily news ([`local/pages/01_Daily_News.py`](local/pages/01_Daily_News.py)) and custom fetching ([`local/pages/02_Custom_Fetch.py`](local/pages/02_Custom_Fetch.py)).
    *   **Deployed**: Streamlit frontend ([`deploy/frontend/Home.py`](deploy/frontend/Home.py)) interacting with a FastAPI backend.
*   **Configurable**:
    *   Local version uses a `config.json` ([`local/config.json`](local/config.json)) for URLs, CSS selectors, and tab configurations.
*   **Model Experimentation**: Includes scripts for preprocessing data ([`models/preprocessing/preprocessing.py`](models/preprocessing/preprocessing.py)) and fine-tuning summarization models like BART ([`models/finetuning/bart.py`](models/finetuning/bart.py)) and LED ([`models/finetuning/led.py`](models/finetuning/led.py)).

## Project Structure

```
NLPApplication/
├── .gitignore
├── LICENSE
├── README.md
├── deploy/                  # Files for the deployed version
│   ├── backend/             # FastAPI backend
│   │   ├── main.py          # FastAPI application
│   │   ├── requirements.txt
│   │   └── scraper.py       # Backend scraping and summarization logic
│   └── frontend/            # Streamlit frontend for deployed version
│       ├── Home.py
│       ├── requirements.txt
│       ├── components/      # UI components for Streamlit
│       ├── pages/           # Streamlit pages
│       ├── tests/           # Frontend tests
│       └── utils/           # Frontend utilities (e.g., API calls)
├── local/                   # Files for local development and testing
│   ├── Home.py              # Main Streamlit app for local version
│   ├── config.json          # Configuration for local app
│   ├── requirements.txt
│   ├── config/              # Configuration utilities for local UI
│   ├── pages/               # Streamlit pages for local version
│   ├── ui/                  # UI layout utilities for local version
│   └── utils/               # Core utilities for local version (scraping, summarization)
└── models/                  # Machine learning models and scripts
    ├── finetuning/          # Scripts for fine-tuning models
    ├── preprocessing/       # Data preprocessing scripts
    └── testing/             # Scripts for testing models
```

## Technologies Used

*   **Python**
*   **Local Version**:
    *   Streamlit: For the user interface.
    *   Crawl4AI, BeautifulSoup4: For web scraping.
    *   Transformers (Hugging Face): For using the fine-tuned BART summarization model.
    *   NLTK, Pandas, Scikit-learn: For text processing and data handling.
*   **Deployed Version**:
    *   FastAPI: For the backend API.
    *   Streamlit: For the frontend user interface.
    *   HTTPX, BeautifulSoup4: For backend web scraping.
    *   OpenAI API: For summarization.
*   **General**: Git, Docker (implied for potential deployment).

## Setup and Installation

### Prerequisites

*   Python 3.8+
*   pip

### Local Development Version

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd NLPApplication/local
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    The `local/requirements.txt` file appears to have some encoding issues. Ensure it's a plain text file with one package per line, then run:
    ```bash
    pip install -r requirements.txt
    ```
    You may need to manually clean up `local/requirements.txt` first. It should look something like:
    ```txt
    fastapi==0.115.1
    httpx==0.28.1
    openai==1.75.0
    # ... and so on for all packages
    ```
4.  **Configure `local/config.json`** with your desired URLs and CSS selectors.
5.  **Run the Streamlit application:**
    ```bash
    streamlit run Home.py
    ```

### Deployed Version (Conceptual - requires backend to be running)

#### Backend (`deploy/backend`)

1.  **Navigate to the backend directory:**
    ```bash
    cd NLPApplication/deploy/backend
    ```
2.  **Create and activate a virtual environment.**
3.  **Install dependencies:**
    Clean up `deploy/backend/requirements.txt` if it has encoding issues, then:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    *   `OPENAI_API_KEY`: Your OpenAI API key (required for summarization).
5.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

#### Frontend (`deploy/frontend`)

1.  **Navigate to the frontend directory:**
    ```bash
    cd NLPApplication/deploy/frontend
    ```
2.  **Create and activate a virtual environment.**
3.  **Install dependencies:**
    Clean up `deploy/frontend/requirements.txt` if it has encoding issues, then:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ensure the backend is running and accessible.** The frontend makes API calls to `https://nlpapplication-0xrw.onrender.com`.
5.  **Run the Streamlit application:**
    ```bash
    streamlit run Home.py
    ```

## Usage

### Local Version

*   Open the Streamlit application in your browser (usually `http://localhost:8501`).
*   **Daily News**: Navigate to the "Daily News" page. It will display news from sources configured in `local/config.json`. Click "More details" to scrape and summarize an article.
*   **Custom Fetch**: Navigate to the "Custom Fetch" page. Enter a URL to scrape and summarize its content directly.

### Deployed Version

*   Access the Streamlit frontend URL (once deployed).
*   **Daily News**: Select a news category (e.g., Politics, Sports). Articles will be fetched from the backend. Click "Read more" to view the summarized content.
*   **Scrape Specific Article**: Enter a direct CNN article URL to fetch and display its summarized content.

## Models

The `models/` directory contains scripts related to:
*   **Preprocessing** ([`models/preprocessing/preprocessing.py`](models/preprocessing/preprocessing.py)): Data cleaning and preparation for model training, including TF-IDF and cosine similarity analysis.
*   **Finetuning** ([`models/finetuning/`](models/finetuning/)): Scripts for fine-tuning sequence-to-sequence models like BART ([`models/finetuning/bart.py`](models/finetuning/bart.py)) and LED ([`models/finetuning/led.py`](models/finetuning/led.py)) on summarization tasks.
*   **Testing** ([`models/testing/`](models/testing/)): Simple scripts to test the inference of pre-trained or fine-tuned models like BART ([`models/testing/bart.py`](models/testing/bart.py)) and LED ([`models/testing/led.py`](models/testing/led.py)).

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.