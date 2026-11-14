from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.recently_viewed_page import RecentlyViewedPage


class ProductPage(BasePage):
    ADD_TO_CART = (By.CSS_SELECTOR, ".add-to-cart-button")
    NOTIFICATION = (By.CSS_SELECTOR, "#bar-notification .content")
    CART_LINK = (By.CSS_SELECTOR, ".header-links .ico-cart")
    RECENTLY_VIEWED_LINK = (By.CSS_SELECTOR, "a[href='/recentlyviewedproducts']")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        self.wait.until(EC.text_to_be_present_in_element(
            self.NOTIFICATION, "The product has been added to your shopping cart"
        ))
        return self

    def open_cart(self):
        self.click((By.CSS_SELECTOR, "#bar-notification .close"))
        self.wait.until(EC.invisibility_of_element_located((By.ID, "bar-notification")))
        self.click(self.CART_LINK)
        return CartPage(self.driver, self.base_url)

    def open_recently_viewed(self):
        self.click(self.RECENTLY_VIEWED_LINK)
        return RecentlyViewedPage(self.driver, self.base_url)
