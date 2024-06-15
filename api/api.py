from fastapi import FastAPI
from crawler.crawler import get_stores, get_stocks

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.get('/crawl')
def crawl(plz):
    stores = get_stores(int(plz))
    stocks = get_stocks(stores)
    return stocks
