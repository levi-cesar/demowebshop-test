from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class RecentlyViewedPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".page-title h1")
    PRODUCTS = (By.CSS_SELECTOR, ".recently-viewed-products-page .product-title a")

    @property
    def title(self):
        return self.visible(self.TITLE).text

    @property
    def product_names(self):
        products = self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCTS))
        return [product.text for product in products]
