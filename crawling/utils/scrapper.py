import json
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from .text_preprocessing import extract_links_from_markdown

def get_links_from_homepage(url, css_selector):
    async def helper_func():
        browser_config = BrowserConfig(headless=True)
        crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector=css_selector
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=crawler_config
            )
            links_list = extract_links_from_markdown(result.markdown)
            with open("links.json", "w") as f:
                json.dump(links_list, f, indent=4)
    
    asyncio.run(helper_func())
    