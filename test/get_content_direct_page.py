import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main(url):
    config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            options={
                'ignore_images': True,
            }
        )
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            print("Raw Markdown Output:\n")
            with open("output.md", "w") as f:
                f.write(result.markdown)
            print("Markdown file generated successfully. Saved in output.md")
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    url = "https://edition.cnn.com/?refresh=1"
    asyncio.run(main(url))