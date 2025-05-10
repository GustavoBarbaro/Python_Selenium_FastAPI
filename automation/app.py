"""Application entry point and FastAPI initialization.

This module sets up the FastAPI app, registers endpoints, and manages
the application lifecycle using a lifespan context manager.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Query

from builder.pool import init_pool, shutdown_pool
from executer.service import driver_to_scrape
from models.product import Product


@asynccontextmanager
async def lifespan(_api: FastAPI) -> AsyncIterator[None]:
    """Lifespan event handler for FastAPI.

    This function initializes the webdriver pool before the application starts
    and shuts it down when the application stops.
    """
    #run BEFORE system start
    init_pool()

    yield
    #run BEFORE system stop
    shutdown_pool()



api = FastAPI(lifespan=lifespan)


@api.get("/scrape")
async def scrape(category: str = Annotated[str, Query(...)]) -> list[Product]:
    """Endpoint to scrape products from a given category."""
    return await driver_to_scrape(category)


