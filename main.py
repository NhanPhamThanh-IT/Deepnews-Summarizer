from fastapi import FastAPI
from scraper import scrape_cnn_articles

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the CNN News Scraper API!"}

@app.get("/scrape")
async def get_articles():
    articles = scrape_cnn_articles()
    return {"articles": articles}
