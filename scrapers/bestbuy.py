from pipeline import pipeline
from pyppeteer import launch


async def scrape_bestby(product):
    async def parse_bestby_product(product):
        try:
            product_title_element = await product.querySelector("h4.sku-title > a")
            product_price_element = await product.querySelector("div.priceView-hero-price > span")
            product_image_element = await product.querySelector("img.product-image")
            product_link_element = await product.querySelector("a.image-link")

            # Will return none if this isn't true TODO:// Fix
            if product_title_element and product_price_element and product_image_element and product_link_element:
                return {
                    "title": await page.evaluate('(element) => element.textContent', product_title_element),
                    "price": await page.evaluate('(element) => element.textContent', product_price_element),
                    "image": await page.evaluate('(element) => element.getAttribute("src")', product_image_element),
                    "link": bestby_url + await page.evaluate('(element) => element.getAttribute("href")', product_link_element),
                }
        except Exception as e:
            print(f"Error in parse_bestby_product: {e}")

    bestby_url = "https://www.bestbuy.com"
    url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }

    data = []

    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.setExtraHTTPHeaders(headers)
        await page.goto(url)

        products = await page.querySelectorAll("li[data-sku-id]")

        for product in products:
            product_data = await parse_bestby_product(product)

            if product_data is not None:
                product_data_cleaned = pipeline(product_data)

                data.append(product_data_cleaned)

        await browser.close()

        return data
    except Exception as e:
        print(f"Error in scrape_bestby {e}")
