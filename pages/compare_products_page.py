from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CompareProductsPage(BasePage):
    PAGE_BODY = (By.CSS_SELECTOR, ".compare-products-page .page-body")
    CLEAR_LIST = (By.CSS_SELECTOR, ".clear-list")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".compare-products-table tr.product-name a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".compare-products-table tr.product-price td")

    @property
    def is_empty(self):
        return "You have no items to compare." in self.visible(self.PAGE_BODY).text

    @property
    def is_clear_list_visible(self):
        return self.visible(self.CLEAR_LIST).is_displayed()

    @property
    def product_names(self):
        self.visible(self.PRODUCT_NAMES)
        return [el.text.strip() for el in self.driver.find_elements(*self.PRODUCT_NAMES)]

    @property
    def product_prices(self):
        self.visible(self.PRODUCT_PRICES)
        # Ignora a primeira coluna que contém apenas o texto "Price"
        price_cells = self.driver.find_elements(*self.PRODUCT_PRICES)[1:]
        return [Decimal(cell.text.strip().replace(",", "")) for cell in price_cells]

    def clear_list(self):
        self.click(self.CLEAR_LIST)
        return self