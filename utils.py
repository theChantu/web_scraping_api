from pyppeteer import launch
from scrapers.amazon import scrape_amazon
from scrapers.bestbuy import scrape_bestby
from scrapers.newegg import scrape_newegg


async def main():
    # Can add a limit= to limit the amount of results [:limit]
    # url = "https://www.newegg.com/p/pl?d=rtx"
    # await download_html(url)
    data = await scrape_newegg("RTX")
    print(data)


async def download_html(url):
    path_name = url.split("https://www.")[1].split(".")[0]

    # Set up headless Chrome options
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }

    try:
        browser = await launch(headless=True)

        page = await browser.newPage()

        await page.setExtraHTTPHeaders(headers)

        await page.goto(url)

        # Get the HTML content of the page
        html_content = await page.content()

        # Save to a file
        with open(f"./htmls/{path_name}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

        await browser.close()

        print("Saved HTML successfully")
    except Exception as e:
        print(f"Error in download_html: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
