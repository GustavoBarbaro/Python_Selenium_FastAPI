
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


POOL_SIZE = 4



def setup_webdriver():

    #initialize and configure webdriver

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    service = Service(ChromeDriverManager().install())

    return options, service

