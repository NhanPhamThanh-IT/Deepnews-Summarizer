import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from .text_preprocessing import extract_links_from_markdown, merge_in_one_paragraph
from .summarize import summarize_by_bart_finetune

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

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Không có loop nào đang chạy
        loop = None

    if loop and loop.is_running():
        # Nếu đang trong event loop (rất hiếm trong Streamlit), dùng task và đợi
        return asyncio.run_coroutine_threadsafe(helper_func(url, css_selector), loop).result()
    else:
        # Bình thường sẽ chạy vào đây trong Streamlit
        return asyncio.run(helper_func(url, css_selector))

def get_content_from_direct_url(url):
    async def helper_func(url):
        browser_config = BrowserConfig(headless=True)
        crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector=".vossi-paragraph",
            exclude_internal_links=True,
            exclude_external_links=True,
            exclude_external_images=True,
            exclude_social_media_links=True,
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=crawler_config
            )
        
        result = summarize_by_bart_finetune(merge_in_one_paragraph(result.markdown))

        return result

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Không có loop nào đang chạy
        loop = None

    if loop and loop.is_running():
        # Nếu đang trong event loop (rất hiếm trong Streamlit), dùng task và đợi
        return asyncio.run_coroutine_threadsafe(helper_func(url), loop).result()
    else:
        # Bình thường sẽ chạy vào đây trong Streamlit
        return asyncio.run(helper_func(url))