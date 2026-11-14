from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class CatalogPage(BasePage):
    SEARCH_INPUT = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-box-button")
    COMPUTERS = (By.CSS_SELECTOR, ".top-menu > li > a[href='/computers']")
    SUBCATEGORIES = (By.CSS_SELECTOR, ".sub-category-item .title a")
    NOTEBOOKS = (By.CSS_SELECTOR, ".sub-category-item a[href='/notebooks']")
    BOOKS = (By.CSS_SELECTOR, ".top-menu > li > a[href='/books']")
    TITLE = (By.CSS_SELECTOR, ".page-title h1")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb a, .breadcrumb strong")
    PRODUCTS = (By.CSS_SELECTOR, ".product-item .product-title a")
    PRICES = (By.CSS_SELECTOR, ".product-item .actual-price")
    UNDER_25 = (By.LINK_TEXT, "Under 25.00")
    REMOVE_FILTER = (By.LINK_TEXT, "Remove Filter")
    SORT_FIELD = (By.ID, "products-orderby")

    def search(self, term):
        self.visible(self.SEARCH_INPUT).send_keys(term)
        self.click(self.SEARCH_BUTTON)

    def open_computers(self):
        self.click(self.COMPUTERS)

    def open_notebooks(self):
        self.click(self.NOTEBOOKS)

    def open_books(self):
        self.click(self.BOOKS)

    def filter_under_25(self):
        self.click(self.UNDER_25)

    def remove_filter(self):
        self.click(self.REMOVE_FILTER)

    def sort_products(self, option):
        sort_select = self.driver.find_element(*self.SORT_FIELD)
        Select(sort_select).select_by_visible_text(option)
        WebDriverWait(self.driver, 10).until(EC.url_contains("orderby=11"))

        updated_select = self.driver.find_element(*self.SORT_FIELD)
        selected_sort = Select(updated_select).first_selected_option.text.strip()
        assert selected_sort == option, f"Esperado '{option}', mas exibiu '{selected_sort}'"

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