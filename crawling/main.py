import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from utils import get_all_links, save_file

with open('config.json', 'r') as file:
    config = json.load(file)

FILE_PATH = config["FILE_PATH"]
NEWS_URL = config["NEWS_URL"]
THRESHOLD = config["THRESHOLD"]
EXCLUDED_TAGS = config["EXCLUDED_TAGS"]

prune_filter = PruningContentFilter(
    threshold=THRESHOLD["VALUE"],           
    threshold_type=THRESHOLD["TYPE"],        
)

md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

async def get_links_from_homepage():
    config = CrawlerRunConfig(
        excluded_tags=EXCLUDED_TAGS,
        exclude_external_links=True,
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=NEWS_URL, 
            config=config
        )

        if result.success:
            links = get_all_links(result.markdown.fit_markdown)
            return links
        else:
            print("Error:", result.error_message)

async def parallel_crawling_for_multipage(urls=None):
    run_conf = CrawlerRunConfig(
        excluded_tags=EXCLUDED_TAGS,
        exclude_external_links=True,
        cache_mode=CacheMode.BYPASS,
        stream=True,
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown.fit_markdown)}")
                save_file(f"output/test/{result.url.split('/')[-1]}.md", result.markdown.fit_markdown)
            else:
                print(f"[ERROR] {result.url} => {result.error_message}")

if __name__ == "__main__":
    urls = asyncio.run(get_links_from_homepage())
    asyncio.run(parallel_crawling_for_multipage(urls))
