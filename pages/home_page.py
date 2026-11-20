from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class HomePage(BasePage):
    NEWSLETTER_EMAIL = (By.ID, "newsletter-email")
    NEWSLETTER_SUBSCRIBE_BUTTON = (By.ID, "newsletter-subscribe-button")
    NEWSLETTER_RESULT = (By.ID, "newsletter-result-block")

    def submit_invalid_newsletter_email(self, email):
        email_field = self.visible(self.NEWSLETTER_EMAIL)
        email_field.clear()
        email_field.send_keys(email)
        self.click(self.NEWSLETTER_SUBSCRIBE_BUTTON)

        self.wait.until(EC.text_to_be_present_in_element(
            self.NEWSLETTER_RESULT, "Enter valid email"
        ))
        return self.visible(self.NEWSLETTER_RESULT).text.strip()