from fastapi import FastAPI
from crawler.crawler import get_stores, get_stocks

app = FastAPI()

@app.get("/")
def index():
    """
    Root endpoint that returns the status of the API.

    Returns:
        dict: A dictionary indicating the status of the API.
    """
    return {"status": "ok"}

@app.get('/crawl')
def crawl(plz: str):
    """
    Endpoint to retrieve stock information based on postal code.

    Args:
        plz (str): The postal code to search for stores and stock levels.

    Returns:
        dict: A dictionary with store addresses as keys and stock levels as values.
    """
    stores = get_stores(int(plz))
    stocks = get_stocks(stores)
    return stocks
