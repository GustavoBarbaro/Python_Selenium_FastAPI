"""pool.py.

This module manages a pool of Selenium WebDriver instances.
"""

from __future__ import annotations

from queue import Queue
from threading import Lock
from typing import TYPE_CHECKING

from selenium import webdriver

from automation.logger import job_id_var, logger
from automation.settings import POOL_SIZE, setup_webdriver

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

_pool = Queue()
_lock = Lock()


def init_pool() -> None:
    """Initialize the WebDriver pool."""
    options, service = setup_webdriver()

    p_size = POOL_SIZE

    for _ in range(p_size):
        driver = webdriver.Chrome(service=service, options=options)
        _pool.put(driver)


def get_available_worker() -> WebDriver | None:
    """Get an available WebDriver instance from the pool."""
    with _lock:
        if _pool.empty():
            logger.error(
                f"Worker {job_id_var.get()} tried to get a driver from an empty pool")
            return None
        logger.info(f"Worker {job_id_var.get()} is getting a driver from the pool")
        logger.debug(f"Pool size: {_pool.qsize() - 1}")
        return _pool.get()


def return_worker(driver: WebDriver) -> None:
    """Return a WebDriver instance to the pool."""
    with _lock:
        _pool.put(driver)

        logger.info(f"Worker {job_id_var.get()} is returning a driver to the pool")
        logger.debug(f"Pool size: {_pool.qsize()}")



def shutdown_pool() -> None:
    """Shutdown the WebDriver pool."""
    with _lock:
        while not _pool.empty():
            driver = _pool.get()
            driver.quit()
            logger.info(f"Turning off webDrivers. Drivers left: {_pool.qsize()}")
