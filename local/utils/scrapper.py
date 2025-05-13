import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from .text_preprocessing import extract_links_from_markdown, merge_in_one_paragraph
from .summarize import summarize_by_bart_finetune

def get_links_from_homepage(url: str, css_selector: str) -> list:
    """
    Extract all hyperlink URLs from a web page's homepage using a CSS selector.

    Description:
    -----------
    This function launches an asynchronous headless browser to crawl a webpage specified by `url`,
    then filters the content based on the provided `css_selector` and extracts hyperlinks
    using markdown parsing.

    Parameters:
    ----------
    url : str
        The URL of the homepage to crawl.
    css_selector : str
        The CSS selector used to target the elements from which to extract links.

    Returns:
    -------
    list of str
        A list of URLs (links) extracted from the selected content.

    Behavior:
    --------
    - Sets up a headless browser using `BrowserConfig`.
    - Bypasses cache to ensure fresh data.
    - Uses `extract_links_from_markdown()` to parse and extract links.
    - Handles both standard and running event loops (for compatibility in notebook or async environments).

    Example:
    --------
    >>> get_links_from_homepage("https://example.com", "div.article > a")
    ['https://example.com/page1', 'https://example.com/page2']
    """
    async def helper_func(url: str, css_selector: str) -> list:
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
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return asyncio.run_coroutine_threadsafe(helper_func(url, css_selector), loop).result()
    else:
        return asyncio.run(helper_func(url, css_selector))

def get_content_from_direct_url(url: str) -> str:
    """
    Crawl and summarize the main content from a direct article URL.

    Description:
    -----------
    This function crawls a specific article or content page using a headless browser,
    extracts the main body content using a predefined CSS selector, and summarizes it
    using a fine-tuned BART model.

    Parameters:
    ----------
    url : str
        The direct URL to a content-rich webpage (such as a news article).

    Returns:
    -------
    str
        A summarized version of the main content from the page.

    Behavior:
    --------
    - Uses a headless browser to crawl the page.
    - Targets paragraphs using `.vossi-paragraph` CSS class.
    - Excludes all types of links and external images to focus purely on text.
    - Merges extracted markdown into one paragraph before summarization.
    - Summarizes using `summarize_by_bart_finetune`.

    Example:
    --------
    >>> get_content_from_direct_url("https://example.com/news/article")
    'This article discusses the latest developments in...'
    """
    async def helper_func(url: str) -> str:
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
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return asyncio.run_coroutine_threadsafe(helper_func(url), loop).result()
    else:
        return asyncio.run(helper_func(url))
