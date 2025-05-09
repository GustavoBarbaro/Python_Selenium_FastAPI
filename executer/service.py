from builder.pool import get_available_worker, return_worker
from builder.scraper import scrape_products
from automation.settings import pool_size
from fastapi import HTTPException

import asyncio



async def driver_to_scrape(category: str):

    driver = get_available_worker()

    if not driver:
        raise HTTPException(status_code=429, detail="no worker available")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, scrape_products, category, driver)
        return result
    finally:
        return_worker(driver)


