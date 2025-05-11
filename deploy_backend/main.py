from fastapi import FastAPI
from scraper import scrape_cnn_articles, scrape_direct_cnn_article_content

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the CNN News Scraper API!"}

@app.get("/scrape")
async def get_articles(url="https://edition.cnn.com/us"):
    articles = await scrape_cnn_articles(url)
    return {"articles": articles}

@app.get("/scrape-article")
async def get_direct_article_content(url: str):
    content = await scrape_direct_cnn_article_content(url)
    return {"content": content}