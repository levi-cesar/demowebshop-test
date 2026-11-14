from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.recently_viewed_page import RecentlyViewedPage
from pages.compare_products_page import CompareProductsPage

class ProductPage(BasePage):
    ADD_TO_CART = (By.CSS_SELECTOR, ".add-to-cart-button")
    ADD_TO_COMPARE = (By.CSS_SELECTOR, ".add-to-compare-list-button")
    NOTIFICATION = (By.CSS_SELECTOR, "#bar-notification .content")
    CART_LINK = (By.CSS_SELECTOR, ".header-links .ico-cart")
    RECENTLY_VIEWED_LINK = (By.CSS_SELECTOR, "a[href='/recentlyviewedproducts']")
    PRICE = (By.CSS_SELECTOR, ".price-value-16")

    # Campos dropdown (<select>)
    PROCESSOR_FIELD = (By.ID, "product_attribute_16_5_4")
    RAM_FIELD = (By.ID, "product_attribute_16_6_5")

    # Opções de HDD (radio buttons)
    HDD_OPTIONS = {
        "18": (By.ID, "product_attribute_16_3_6_18"),  # 320 GB
        "19": (By.ID, "product_attribute_16_3_6_19"),  # 400 GB [+100.00]
    }

    # Opções de OS (radio buttons)
    OS_OPTIONS = {
        "44": (By.ID, "product_attribute_16_4_7_44"),  # Ubuntu
        "20": (By.ID, "product_attribute_16_4_7_20"),  # Windows 7 [+50.00]
        "21": (By.ID, "product_attribute_16_4_7_21"),  # Windows 10 [+60.00]
    }

    # Opções de Software (checkboxes)
    SOFTWARE_OPTIONS = {
        "22": (By.ID, "product_attribute_16_8_8_22"),  # Microsoft Office [+50.00]
        "23": (By.ID, "product_attribute_16_8_8_23"),  # Acrobat Reader [+10.00]
        "24": (By.ID, "product_attribute_16_8_8_24"),  # Total Commander [+5.00]
    }

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

    def desktop_select_processor(self, option):
        processor_field = self.visible(self.PROCESSOR_FIELD)
        Select(processor_field).select_by_value(option)
        return self

    def desktop_select_ram(self, option):
        ram_field = self.visible(self.RAM_FIELD)
        Select(ram_field).select_by_value(option)
        return self

    def desktop_select_hdd(self, option):
        self.click(self.HDD_OPTIONS[option])
        return self

    def desktop_select_os(self, option):
        self.click(self.OS_OPTIONS[option])
        return self

    def desktop_select_software(self, options):
        for key, locator in self.SOFTWARE_OPTIONS.items():
            checkbox = self.visible(locator)
            should_be_checked = key in options
            if checkbox.is_selected() != should_be_checked:
                checkbox.click()
        return self

    def add_to_compare_list(self):
        self.click(self.ADD_TO_COMPARE)
        self.wait.until(EC.url_contains("/compareproducts"))
        return CompareProductsPage(self.driver, self.base_url)

    @property
    def notification_text(self):
        return self.visible(self.NOTIFICATION).text.strip()

    @property
    def header_cart_text(self):
        return self.visible(self.CART_LINK).text.strip()

    @property
    def price(self):
        return Decimal(self.visible(self.PRICE).text.replace(",", ""))