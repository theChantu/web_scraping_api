from pipeline import pipeline
from pyppeteer import launch


async def scrape_newegg(product):
    async def parse_newegg_product(product):
        try:
            product_title_element = await product.querySelector("a.item-title")
            product_price_element = await product.querySelector("li.price-current strong")
            product_image_element = await product.querySelector("div.item-container img")
            product_link_element = await product.querySelector("a.item-title")

            # Will return none if this isn't true TODO:// Fix
            if product_title_element and product_price_element and product_image_element and product_link_element:
                return {
                    "title": await page.evaluate('(element) => element.textContent', product_title_element),
                    "price": await page.evaluate('(element) => element.textContent', product_price_element),
                    "image": await page.evaluate('(element) => element.getAttribute("src")', product_image_element),
                    "link": await page.evaluate('(element) => element.getAttribute("href")', product_link_element),
                }
        except Exception as e:
            print(f"Error in parse_newegg_product: {e}")

    url = f"https://www.newegg.com/p/pl?d={product}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }

    data = []

    try:
        browser = await launch(headless=True, userDataDir='/tmp/browser-data')
        page = await browser.newPage()
        await page.setExtraHTTPHeaders(headers)
        await page.goto(url)

        products = await page.querySelectorAll("div.item-cell")

        for product in products:
            product_data = await parse_newegg_product(product)

            if product_data is not None:
                product_data_cleaned = pipeline(product_data)

                data.append(product_data_cleaned)

        await browser.close()

        return data
    except Exception as e:
        print(f"Error in scrape_newegg {e}")
