from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    LAPTOP_ROW = (By.XPATH, "//table[contains(@class,'cart')]//tr[.//a[normalize-space()='14.1-inch Laptop']]")
    UPDATE_CART = (By.NAME, "updatecart")
    CART_QUANTITY = (By.CSS_SELECTOR, ".header-links .cart-qty")
    COUPON_INPUT = (By.NAME, "discountcouponcode")
    APPLY_COUPON = (By.NAME, "applydiscountcouponcode")
    COUPON_MESSAGE = (By.CSS_SELECTOR, ".coupon-box .message")
    TOTAL = (By.CSS_SELECTOR, ".cart-total .product-price.order-total")
    SUBTOTAL = (By.XPATH, "//table[contains(@class,'cart-total')]//tr[.//*[normalize-space()='Sub-Total:']]//span[contains(@class,'product-price')]")

    @staticmethod
    def money(text):
        return Decimal(text.strip().replace(",", ""))

    def update_laptop_quantity(self, quantity):
        row = self.visible(self.LAPTOP_ROW)
        field = row.find_element(By.CSS_SELECTOR, ".qty-input")
        field.clear()
        field.send_keys(str(quantity))
        self.click(self.UPDATE_CART)
        self.wait.until(EC.staleness_of(row))
        self.wait.until(EC.text_to_be_present_in_element(
            self.CART_QUANTITY, f"({quantity})"
        ))

    @property
    def laptop_total(self):
        row = self.visible(self.LAPTOP_ROW)
        return self.money(row.find_element(By.CSS_SELECTOR, ".product-subtotal").text)

    @property
    def subtotal(self):
        return self.money(self.visible(self.SUBTOTAL).text)

    @property
    def total(self):
        return self.money(self.visible(self.TOTAL).text)

    @property
    def cart_quantity(self):
        return self.visible(self.CART_QUANTITY).text

    def apply_coupon(self, code):
        field = self.visible(self.COUPON_INPUT)
        field.clear()
        field.send_keys(code)
        self.click(self.APPLY_COUPON)
        return self.visible(self.COUPON_MESSAGE).text
