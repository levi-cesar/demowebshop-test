from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    GUEST = (By.CSS_SELECTOR, ".checkout-as-guest-button")

    FIRST_NAME = (By.ID, "BillingNewAddress_FirstName")
    LAST_NAME = (By.ID, "BillingNewAddress_LastName")
    EMAIL = (By.ID, "BillingNewAddress_Email")
    COUNTRY = (By.ID, "BillingNewAddress_CountryId")
    CITY = (By.ID, "BillingNewAddress_City")
    ADDRESS1 = (By.ID, "BillingNewAddress_Address1")
    ZIP = (By.ID, "BillingNewAddress_ZipPostalCode")
    PHONE = (By.ID, "BillingNewAddress_PhoneNumber")
    BILLING_CONTINUE = (By.CSS_SELECTOR, "#billing-buttons-container input.button-1")
    SHIPPING_ADDRESS_CONTINUE = (By.CSS_SELECTOR, "#shipping-buttons-container input.button-1")
    SHIPPING_METHOD_CONTINUE = (By.CSS_SELECTOR, "#shipping-method-buttons-container input.shipping-method-next-step-button")
    PAYMENT_METHOD_CONTINUE = (By.CSS_SELECTOR, "#payment-method-buttons-container input.payment-method-next-step-button")
    PAYMENT_INFO_CONTINUE = (By.CSS_SELECTOR, "#payment-info-buttons-container input.payment-info-next-step-button")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "#confirm-order-buttons-container input.confirm-order-next-step-button")
    RADIO_LABELS = (By.CSS_SELECTOR, "input[type='radio'] + label[for]")
    PAYMENT_INFO = (By.CSS_SELECTOR, "#checkout-payment-info-load .info")
    CONFIRM_TOTAL = (By.CSS_SELECTOR, "#checkout-confirm-order-load .cart-total .product-price.order-total")
    COMPLETED_MESSAGE = (By.CSS_SELECTOR, ".section.order-completed .title")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-completed .details > li:first-child")

    def checkout_as_guest(self):
        self.click(self.GUEST)
        self.wait.until(EC.url_contains("/onepagecheckout"))
        return self

    def fill_billing_address(self, email):
        self.visible(self.FIRST_NAME).send_keys("Aluno")
        self.visible(self.LAST_NAME).send_keys("QA")
        self.visible(self.EMAIL).send_keys(email)
        Select(self.visible(self.COUNTRY)).select_by_visible_text("Brazil")
        self.visible(self.CITY).send_keys("Recife")
        self.visible(self.ADDRESS1).send_keys("Rua Teste, 100")
        self.visible(self.ZIP).send_keys("50000-000")
        self.visible(self.PHONE).send_keys("81999990000")
        self.click(self.BILLING_CONTINUE)
        return self

    def continue_shipping_address(self):
        self.click(self.SHIPPING_ADDRESS_CONTINUE)
        return self

    def _select_radio(self, option_text):
        for label in self.driver.find_elements(*self.RADIO_LABELS):
            if label.is_displayed() and option_text in label.text:
                radio_id = label.get_attribute("for")
                self.click((By.ID, radio_id))
                return

        raise LookupError(f"Opção ausente no checkout: {option_text}")

    def select_ground_and_continue(self):
        self.visible(self.SHIPPING_METHOD_CONTINUE)
        self._select_radio("Ground")
        self.click(self.SHIPPING_METHOD_CONTINUE)
        return self

    def select_cod_and_continue(self):
        self.visible(self.PAYMENT_METHOD_CONTINUE)
        self._select_radio("Cash On Delivery (COD)")
        self.click(self.PAYMENT_METHOD_CONTINUE)
        return self

    def payment_information_message(self):
        return self.visible(self.PAYMENT_INFO).text.strip()

    def continue_payment_information(self):
        self.click(self.PAYMENT_INFO_CONTINUE)
        return self

    @property
    def confirm_total(self):
        text = self.visible(self.CONFIRM_TOTAL).text.strip()
        return Decimal(text.replace(",", ""))

    def confirm_order(self):
        self.click(self.CONFIRM_BUTTON)
        self.wait.until(EC.url_contains("/checkout/completed/"))
        return self

    @property
    def completed_message(self):
        return self.visible(self.COMPLETED_MESSAGE).text.strip()

    @property
    def order_number(self):
        text = self.visible(self.ORDER_NUMBER).text.strip()
        return text.split(":")[-1].strip()