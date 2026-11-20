from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WishlistPage(BasePage):
    ITEM_ROWS = (By.CSS_SELECTOR, "tr.cart-item-row")
    ITEM_NAME = (By.CSS_SELECTOR, "td.product > a")
    ITEM_ATTRIBUTES = (By.CSS_SELECTOR, ".attributes")
    ITEM_UNIT_PRICE = (By.CSS_SELECTOR, ".product-unit-price")

    def product_row(self, product_name):
        self.visible(self.ITEM_ROWS)
        for row in self.driver.find_elements(*self.ITEM_ROWS):
            name = row.find_element(*self.ITEM_NAME).text.strip()
            if name == product_name:
                return row
        raise LookupError(f"Produto ausente na wishlist: {product_name}")

    def product_attributes(self, product_name):
        row = self.product_row(product_name)
        return row.find_element(*self.ITEM_ATTRIBUTES).text.strip()

    def product_unit_price(self, product_name):
        row = self.product_row(product_name)
        price = row.find_element(*self.ITEM_UNIT_PRICE).text.strip()
        return Decimal(price.replace(",", ""))