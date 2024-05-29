from fastapi import FastAPI
from crawler.crawler import get_shops

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.get('/crawl')
def crawl(plz):
    url = "https://www.dm.de/koro-pistazienschnitte-mit-45-prozent-pistazie-p4255582809893.html"
    result = get_shops(url, plz)
    return result
