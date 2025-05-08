import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from .text_preprocessing import extract_links_from_markdown

def get_links_from_homepage(url, css_selector):
    async def helper_func(url, css_selector):
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
        
        return extract_links_from_markdown(result.markdown)
            
    
    return asyncio.run(helper_func(url, css_selector))