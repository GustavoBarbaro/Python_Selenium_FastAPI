from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from builder.pool import init_pool, shutdown_pool
from executer.service import driver_to_scrape



@asynccontextmanager
async def lifespan(api: FastAPI):
    #run BEFORE system start
    init_pool()

    yield
    #run BEFORE system stop
    shutdown_pool()



api = FastAPI(lifespan=lifespan)


@api.get("/scrape")
async def scrape(category: str = Query(...)):

    return await driver_to_scrape(category)


