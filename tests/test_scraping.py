"""Test scraping.

This module contains tests for the scraping endpoint of the FastAPI application.
"""

import asyncio

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient, Response

from automation.app import api  #fastAPI instance
from automation.settings import POOL_SIZE

SUCESS = 200
MANY_REQUESTS = 429

EXTRA_REQUESTS = 2

@pytest.mark.asyncio
async def test_scraping_endpoint_returns_200() -> None:
    """Test if the scraping endpoint returns a 200 status code."""
    async with LifespanManager(api), AsyncClient(
        transport=ASGITransport(app=api),
        base_url="http://test") as ac:

        response = await ac.get("/scrape", params={"category": "Cosmetics"})

    assert response.status_code == SUCESS  # noqa: S101


@pytest.mark.asyncio
async def test_endpoint_reuturn_json() -> None:
    """Test if the scraping endpoint returns a JSON response."""
    async with LifespanManager(api), AsyncClient(
        transport=ASGITransport(app=api),
        base_url="http://test") as ac:

        response = await ac.get("/scrape", params={"category": "Cosmetics"})

    assert isinstance(response.json(), list)  # noqa: S101


@pytest.mark.asyncio
async def test_many_requests_429() -> None:
    """Test if return 429 when use all the pool size."""
    async with LifespanManager(api), AsyncClient(
            transport=ASGITransport(app=api), base_url="http://test") as ac:

            async def make_request() -> Response:
                return await ac.get("/scrape", params={"category": "Cosmetics"})

            #send max + 1 requests simultaneously
            responses = await asyncio.gather(
                *[make_request() for _ in range(POOL_SIZE + EXTRA_REQUESTS)])

    #counting each status code
    status_codes = [response.status_code for response in responses]

    #checking the status codes
    assert status_codes.count(SUCESS) == POOL_SIZE  # noqa: S101
    assert status_codes.count(MANY_REQUESTS) == EXTRA_REQUESTS  # noqa: S101
