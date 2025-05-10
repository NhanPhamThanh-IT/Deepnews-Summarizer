from fastapi import FastAPI
from scraper import scrape_cnn_articles

app = FastAPI()

@app.get("/scrape")
async def get_articles():
    articles = await scrape_cnn_articles()
    return {"articles": articles}
