from fastapi import FastAPI
from scrapers.amazon import scrape_amazon
from scrapers.bestbuy import scrape_bestby
from scrapers.newegg import scrape_newegg

app = FastAPI()


@app.get("/amazon/{asin}")
async def fetch_amazon(asin: str):
    try:
        # TODO:// allow pass in of header as arg from random header API
        # TODO:// add a limit arg to limit amount of products returned
        data = await scrape_amazon(asin)
        return data
    except Exception as e:
        return {"Error": f"Unable to fetch: {e}"}


@app.get("/bestby/{asin}")
async def fetch_bestby(asin: str):
    try:
        data = await scrape_bestby(asin)
        return data
    except Exception as e:
        return {"Error": f"Unable to fetch: {e}"}


@app.get("/newegg/{asin}")
async def fetch_newegg(asin: str):
    try:
        data = await scrape_newegg(asin)
        return data
    except Exception as e:
        return {"Error": f"Unable to fetch: {e}"}
