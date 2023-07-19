from pipeline import pipeline
from pyppeteer import launch


async def scrape_amazon(product):
    async def parse_amazon_product(product):
        try:
            product_title_element = await product.querySelector("span.a-size-medium.a-color-base.a-text-normal")
            product_price_element = await product.querySelector("span.a-offscreen")
            product_image_element = await product.querySelector("img.s-image")
            product_link_element = await product.querySelector("a.a-link-normal")

            # Will return none if this isn't true TODO:// Fix
            if product_title_element and product_price_element and product_image_element and product_link_element:
                return {
                    "title": await page.evaluate('(element) => element.textContent', product_title_element),
                    "price": await page.evaluate('(element) => element.textContent', product_price_element),
                    "image": await page.evaluate('(element) => element.getAttribute("src")', product_image_element),
                    "link": amazon_url + await page.evaluate('(element) => element.getAttribute("href")', product_link_element),
                }
        except Exception as e:
            print(f"Error in parse_amazon_product: {e}")

    amazon_url = "https://www.amazon.com"
    url = f"https://www.amazon.com/s?k={product}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }

    data = []

    try:
        browser = await launch(headless=True, userDataDir='/tmp/browser-data')
        page = await browser.newPage()
        await page.setExtraHTTPHeaders(headers)
        await page.goto(url)

        products = await page.querySelectorAll("div[data-uuid]")

        for product in products:
            product_data = await parse_amazon_product(product)

            if product_data is not None:
                product_data_cleaned = pipeline(product_data)

                data.append(product_data_cleaned)

        await browser.close()

        return data
    except Exception as e:
        print(f"Error in scrape_amazon {e}")
