from fastapi import FastAPI
from scraper import scrape_cnn_articles

app = FastAPI()

@app.get("/scrape")
def get_articles():
    articles = scrape_cnn_articles()
    return {"articles": articles}
