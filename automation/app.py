from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from executer.service import setup_webdriver, end_webdriver
from builder.scraper import scrape_products





@asynccontextmanager
async def lifespan(api: FastAPI):
    #run BEFORE system start
    api.state.driver = setup_webdriver()


    yield
    #run AFTER system stop
    end_webdriver(api.state.driver)



api = FastAPI(lifespan=lifespan)


@api.get("/scrape")
async def scrape(category: str, request:Request):

    driver = api.state.driver

    return scrape_products(category, driver)