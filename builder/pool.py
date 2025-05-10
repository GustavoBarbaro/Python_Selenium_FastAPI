"""pool.py.

This module manages a pool of Selenium WebDriver instances.
"""

from __future__ import annotations

from queue import Queue
from threading import Lock
from typing import TYPE_CHECKING

from selenium import webdriver

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
            return None
        return _pool.get()


def return_worker(driver: WebDriver) -> None:
    """Return a WebDriver instance to the pool."""
    with _lock:
        _pool.put(driver)



def shutdown_pool() -> None:
    """Shutdown the WebDriver pool."""
    with _lock:
        while not _pool.empty():
            driver = _pool.get()
            driver.quit()
