# scraper.py
import httpx
from bs4 import BeautifulSoup

async def scrape_cnn_articles():
    url = "https://edition.cnn.com/world"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for link in soup.select("h3 a"):
            href = link.get("href")
            title = link.text.strip()
            if href and title:
                articles.append({
                    "title": title,
                    "url": f"https://edition.cnn.com{href}" if href.startswith("/") else href
                })

        return articles
