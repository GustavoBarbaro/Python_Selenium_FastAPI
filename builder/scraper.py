"""scraper.py.

This module contains web scraping logic.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from models.product import Product


def scrape_products(category: str, driver: WebDriver) -> list[Product]:
    """Scrape products from the given category.

    receive the category name and the driver instance
    and return a list of products.
    """
    driver.get("https://selenium-html-test.replit.app/")

    wait = WebDriverWait(driver, 10)

    products = wait.until(EC.presence_of_all_elements_located((By.ID, "product-table")))


    #filter table by category
    filter_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='category-filter']")))

    filter_button.click()

    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//span[(text())='{category}'][1]")))
    option.click()


    #to save table data
    products: list[Product] = []


    #find if have pagination
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "button[data-page]")))

    pages = driver.find_elements(By.CSS_SELECTOR, "button[data-page]")

    #iterate through the pages
    for page in pages:

        page.click()

        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@id='product-table']/tbody/tr")))

        rows = driver.find_elements(By.XPATH, "//table[@id='product-table']/tbody/tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            raw_price = cols[3].text.replace("$", "").strip()
            price = float(raw_price)

            product = Product (
                ID = cols[0].text,
                Name = cols[1].text,
                Category = cols[2].text,
                Price = price,
                Stock = cols[4].text,
            )

            products.append(product)

    return products




