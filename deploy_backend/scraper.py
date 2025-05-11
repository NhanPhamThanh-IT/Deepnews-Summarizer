import httpx
from bs4 import BeautifulSoup

async def scrape_cnn_articles(url: str = "https://edition.cnn.com/us") -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for a_tag in soup.select("a.container__link--type-article"):
            href = a_tag.get("href")
            headline_span = a_tag.select_one("span.container__headline-text")
            title = headline_span.get_text(strip=True) if headline_span else None

            if href and title:
                full_url = f"https://edition.cnn.com{href}" if href.startswith("/") else href
                articles.append({
                    "title": title,
                    "url": full_url
                })

        return articles

async def scrape_direct_cnn_articles(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for a_tag in soup.select("a.container__link--type-article"):
            href = a_tag.get("href")
            headline_span = a_tag.select_one("span.container__headline-text")
            title = headline_span.get_text(strip=True) if headline_span else None

            if href and title:
                full_url = f"https://edition.cnn.com{href}" if href.startswith("/") else href
                articles.append({
                    "title": title,
                    "url": full_url
                })

        return articles