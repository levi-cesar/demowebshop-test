from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CatalogPage(BasePage):
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-box-button")
    COMPUTERS = (By.CSS_SELECTOR, ".top-menu > li > a[href='/computers']")
    SUBCATEGORIES = (By.CSS_SELECTOR, ".sub-category-item .title a")
    NOTEBOOKS = (By.CSS_SELECTOR, ".sub-category-item a[href='/notebooks']")
    TITLE = (By.CSS_SELECTOR, ".page-title h1")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb a, .breadcrumb strong")
    PRODUCTS = (By.CSS_SELECTOR, ".product-item .product-title a")
    PRICES = (By.CSS_SELECTOR, ".product-item .actual-price")
    UNDER_25 = (By.LINK_TEXT, "Under 25.00")
    REMOVE_FILTER = (By.LINK_TEXT, "Remove Filter")

    def search(self, term):
        self.visible(self.SEARCH_INPUT).send_keys(term)
        self.click(self.SEARCH_BUTTON)

    def open_computers(self):
        self.click(self.COMPUTERS)

    def open_notebooks(self):
        self.click(self.NOTEBOOKS)

    def filter_under_25(self):
        self.click(self.UNDER_25)

    def remove_filter(self):
        self.click(self.REMOVE_FILTER)

    @property
    def title(self):
        return self.visible(self.TITLE).text

    @property
    def subcategories(self):
        elements = self.wait.until(EC.visibility_of_all_elements_located(self.SUBCATEGORIES))
        return [element.text for element in elements]

    @property
    def breadcrumb(self):
        elements = self.wait.until(EC.visibility_of_all_elements_located(self.BREADCRUMB))
        return [element.text.upper() for element in elements]

    @property
    def product_names(self):
        elements = self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCTS))
        return [element.text for element in elements]

    @property
    def prices(self):
        elements = self.wait.until(EC.visibility_of_all_elements_located(self.PRICES))
        return [Decimal(element.text.replace(",", "")) for element in elements]