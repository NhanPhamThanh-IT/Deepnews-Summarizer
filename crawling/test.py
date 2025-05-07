import re
from bs4 import BeautifulSoup
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from utils import save_file

with open('config.json', 'r') as file:
    config = json.load(file)

FILE_PATH = "test.md"
NEWS_URL = "https://edition.cnn.com/2025/05/06/us/inside-the-multi-day-meltdown-at-newark-airport"
THRESHOLD = config["THRESHOLD"]
EXCLUDED_TAGS = config["EXCLUDED_TAGS"]

prune_filter = PruningContentFilter(
    threshold=THRESHOLD["VALUE"],           
    threshold_type=THRESHOLD["TYPE"],        
)

md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

def clean_text(text):
    patterns_to_remove = [
        r"Ad Feedback", r"Link Copied!", r"Follow:", r"Video Ad Feedback",
        r"Privacy Policy.*", r"Cookie List.*", r"Apply Cancel.*",
        r"checkbox label.*", r"Close.*", r"\*{2}|\*|_{1,3}", r"[^\x00-\x7F]+"
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\n{2,}', '\n', text.strip())
    
    text = re.sub(r'\[(.*?)\]\((https?://[^\s]+)\)', r'\1', text)

    text = BeautifulSoup(text, "html.parser").get_text()

    return text.strip()


async def testing():
    config = CrawlerRunConfig(
        excluded_tags=EXCLUDED_TAGS,
        exclude_external_links=True,
        exclude_social_media_links=True,
        exclude_external_images=True,
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=NEWS_URL, 
            config=config
        )

        if result.success:
            save_file(FILE_PATH,clean_text(result.markdown.fit_markdown))
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(testing())