from builder.pool import get_available_worker, return_worker
from builder.scraper import scrape_products
from fastapi import HTTPException





def driver_to_scrape(category: str):

    driver = get_available_worker()

    if not driver:
        raise HTTPException(status_code=429, detail="no worker available")

    try:
        return scrape_products(category, driver)
    finally:
        return_worker(driver)