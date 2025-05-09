from selenium import webdriver
from queue import Queue
from threading import Lock

from automation.settings import setup_webdriver, pool_size


_pool = Queue()
_lock = Lock()


def init_pool():

    options, service = setup_webdriver()

    p_size = pool_size()

    for _ in range(p_size):
        driver = webdriver.Chrome(service=service, options=options)
        _pool.put(driver)


def get_available_worker():
    with _lock:
        if _pool.empty():
            return None
        return _pool.get()


def return_worker(driver):
    with _lock:
        _pool.put(driver)



def shutdown_pool():
    with _lock:
        while not _pool.empty():
            driver = _pool.get()
            driver.quit()