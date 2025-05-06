import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from utils import save_file

async def quick_parallel_example():
    urls = [
            'https://edition.cnn.com/2025/05/04/us/ohio-rodney-hinton-jr-arrest-hnk',
            'https://edition.cnn.com/2025/05/04/us/ohio-rodney-hinton-jr-arrest-hnk',
            'https://edition.cnn.com/2025/05/05/us/shooting-glendale-arizona-multiple-injured-hnk',
            'https://edition.cnn.com/2025/05/03/us/cultural-events-canceled-trump-deportations',
            'https://edition.cnn.com/2025/05/05/us/trump-alcatraz-prison-history-hnk',
            'https://edition.cnn.com/2025/05/05/us/karen-read-retrial-different',
            'https://edition.cnn.com/2025/05/05/us/5-things-to-know-for-may-5-lady-gaga-plot-alcatraz-trump-budget-weather-forecasting-mike-pence',
            'https://edition.cnn.com/2025/05/04/us/newark-airport-nj-united-flights-delays',
            'https://edition.cnn.com/2025/05/05/us/temple-student-suspended-antisemitic-sign-barstool-portnoy',
            'https://edition.cnn.com/2025/05/04/us/doj-minnesota-hennepin-moriarty-race'
    ]

    prune_filter = PruningContentFilter(
        threshold=0.45,           
        threshold_type="dynamic",        
    )

    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    run_conf = CrawlerRunConfig(
        excluded_tags=["nav", "footer", "header", "script", "style", "svg", "iframe", "canvas", "video", "audio", "picture"],
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
    asyncio.run(quick_parallel_example())
