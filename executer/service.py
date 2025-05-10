"""service.py.

This module contains tretment for manage the web drivers in the pool.
"""

import asyncio

from fastapi import HTTPException

from builder.pool import get_available_worker, return_worker
from builder.scraper import scrape_products
from models.product import Product


async def driver_to_scrape(category: str) -> list[Product]:
    """Get a driver from the pool and use it to scrape products."""
    driver = get_available_worker()

    if not driver:
        raise HTTPException(status_code=429, detail="no worker available")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, scrape_products, category, driver)
        if result == []:
            raise HTTPException(status_code=404, detail="category not found")
        return result
    finally:
        return_worker(driver)


