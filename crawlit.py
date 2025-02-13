import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main(url_to_scrape:str) -> None:
    md_generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": True,
        "escape_html": False,
        "body_width": 80
    }
    )
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )
    async with AsyncWebCrawler() as crawler:
        url = url_to_scrape
        result = await crawler.arun(url,magic=True,remove_overlay_elements=True,
            page_timeout=60000,config=config)

        if result.success:
            print("Raw Markdown Output:\n")
            print(result.markdown)  # The unfiltered markdown from the page
            
            # Write to markdown file
            filename = "output.md"  # You can modify the filename as needed
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.markdown)
            print(f"\nMarkdown has been saved to {filename}")
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main(input('Enter Url To Scrape: ')))