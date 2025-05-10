"""settings.py.

This module contains the settings for configure the chrome webdriver
and the pool size
and the logger configuration.
"""

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

POOL_SIZE = 4

#config logger
LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(threadName)s] [job-id:%(job_id)s] %(message)s"
)

LOG_LEVEL = "DEBUG"



def setup_webdriver() -> tuple[Options, Service]:
    """Configure the chrome webdriver."""
    #initialize and configure webdriver

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service(ChromeDriverManager().install())

    return options, service
