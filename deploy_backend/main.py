from fastapi import FastAPI
from scraper import scrape_cnn_articles

app = FastAPI()

@app.get("/scrape")
async def get_articles(url="https://edition.cnn.com/us"):
    articles = await scrape_cnn_articles(url)
    return {"articles": articles}
