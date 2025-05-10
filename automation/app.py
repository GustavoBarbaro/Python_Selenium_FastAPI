"""Application entry point and FastAPI initialization.

This module sets up the FastAPI app, registers endpoints, and manages
the application lifecycle using a lifespan context manager.
"""

import uuid
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from typing import Annotated, Callable

from fastapi import FastAPI, Query, Request
from starlette.responses import Response

from automation.logger import job_id_var, logger
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


@api.middleware("http")
async def add_job_id_to_context(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware to add a unique job ID to the request context."""
    job_id = str(uuid.uuid4())
    token = job_id_var.set(job_id)

    logger.info("Received request")

    try:
        response = await call_next(request)
    finally:
        job_id_var.reset(token)

    return response



@api.get("/scrape")
async def scrape(category: str = Annotated[str, Query(...)]) -> list[Product]:
    """Endpoint to scrape products from a given category."""
    return await driver_to_scrape(category)


