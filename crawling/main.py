import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from utils import get_all_links

with open('config.json', 'r') as file:
    config = json.load(file)

FILE_PATH = config["FILE_PATH"]
NEWS_URL = config["NEWS_URL"]

async def get_links_from_homepage():
    prune_filter = PruningContentFilter(
        threshold=0.45,           
        threshold_type="dynamic",        
    )

    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    config = CrawlerRunConfig(
        excluded_tags=["nav", "footer", "header", "script", "style", "svg", "iframe", "canvas", "video", "audio", "picture"],
        exclude_external_links=True,

        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=NEWS_URL, 
            config=config
        )

        if result.success:
            links = get_all_links(result.markdown.fit_markdown)

            print(links[:10])
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(get_links_from_homepage())
