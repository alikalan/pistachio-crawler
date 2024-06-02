from fastapi import FastAPI
from crawler.crawler import get_shops
from params import URL

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.get('/crawl')
def crawl(plz):
    url = URL
    result = get_shops(url, plz)
    return result
