import httpx
from bs4 import BeautifulSoup
import openai
import os

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

def summarize(content: str, api_key: str) -> str:
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that summarizes text in clear, neutral English. "
                    "Keep the summary between 50 and 150 words. Do not be creative — just factual."
                )
            },
            {
                "role": "user",
                "content": f"Summarize the following content:\n\n{content}"
            }
        ],
        temperature=0.0,
        max_tokens=300
    )

    summary = response['choices'][0]['message']['content']
    return summary

async def scrape_direct_cnn_article_content(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("p.vossi-paragraph")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return summarize(content, api_key=os.getenv("OPENAI_API_KEY"))