from selenium import webdriver
from queue import Queue
from threading import Lock


from automation.settings import setup_webdriver, POOL_SIZE


_pool = Queue()
_lock = Lock()


def init_pool():

    options, service = setup_webdriver()

    p_size = POOL_SIZE

    for _ in range(p_size):
        driver = webdriver.Chrome(service=service, options=options)
        _pool.put(driver)


def get_available_worker():
    with _lock:
        if _pool.empty():
            return None
        print(f"Pegando WebDriver. Restantes no pool: {_pool.qsize() - 1}")
        return _pool.get()


def return_worker(driver):
    with _lock:
        _pool.put(driver)
        print(f"Devolvendo WebDriver. Total disponíveis: {_pool.qsize()}")



def shutdown_pool():
    with _lock:
        while not _pool.empty():
            driver = _pool.get()
            driver.quit()