from requests_html import AsyncHTMLSession


# Each time data is fetched, possibly just recreate the class object each time? Could be a better way? That way on init you can just pass in whatever keyword to s?k=
class AmazonScraper():

    def __init__(self, url):
        self.url = "https://amazon.com"
        self.product_url = f"https://www.amazon.com/s?k={url}"
        self.session = AsyncHTMLSession()

    async def fetch_data(self):
        data = []

        try:
            response = await self.session.get(self.product_url)
            await response.html.arender(keep_page=True, scrolldown=1)

            products = response.html.find('div.sg-col-inner')

            for product in products:
                # Pass product into the pipeline, to be handled, after the data is returned from fetch_product_data
                product_data = self.fetch_product_data(product)
                if product_data is not None:
                    product_data_cleaned = pipeline(product_data)
                    data.append(product_data_cleaned)

            # Close session
            await self.session.close()

            # Remove none types
            # Can put this in a seperate function later possibly (another pipeline for lists)
            return [product for product in data if product is not None]

        except Exception as e:
            print(f"Error in fetch_data: {e}")
            return None

    def fetch_product_data(self, product_element):
        product_title_element = product_element.find("span.a-size-medium.a-color-base.a-text-normal")
        product_price_element = product_element.find("span.a-offscreen")
        product_image_element = product_element.find("img.s-image")

        if product_title_element and product_price_element and product_image_element:
            return {
                "title": product_title_element[0].text,
                "price": product_price_element[0].text,
                "image": product_image_element[0].attrs.get("src")
            }


def pipeline(product):
    title, price, image = product.values()

    title = title.strip()
    price = float(price.replace("$", "").replace(",", ""))

    new_product = {
        "title": title,
        "price": price,
        "image": image
    }

    return new_product
    # This function will make sure every project has the same elements, like no whitespace, float as currency, etc

def scrape_all():
    pass
    # This function will scrape every website, and return in a big list

# Make a big function that just executes each scraper, and have each scraper be it's own py file

# async def main():
#     scraper = AmazonScraper("graphics+card")
#     data = await scraper.fetch_data()
#     print(data)
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(main())
