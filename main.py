from fastapi import FastAPI
import requests
from scraper import AmazonScraper

app = FastAPI()


@app.get("/{asin}")
async def get_data(asin: str):
    try:
        scraper = AmazonScraper(asin)
        data = await scraper.fetch_data()
        return data
    except KeyError:
        return {"Error": "Unable to parse page"}
