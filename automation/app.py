from fastapi import FastAPI, Query
from builder.scraper import scrape_products



api = FastAPI()

def analyse(category: str):

    # Simulate some analysis
    if category == "sports":
        return {"category": category, "data": "Sports data"}
    elif category == "news":
        return {"category": category, "data": "News data"}
    else:
        return {"error": "Category not found"}




@api.get("/scrape")
def scrape(category: str):

    return scrape_products(category)