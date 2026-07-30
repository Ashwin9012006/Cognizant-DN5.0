"""
Hands-On 7 – pages/input_form_page.py
Page Object for the Input Form Submit page.

Step 57: Methods fill_form(), submit_form(), get_success_message()
Fields: name, email, phone, address
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class InputFormPage(BasePage):
    """
    Page Object for: https://www.lambdatest.com/selenium-playground/input-form-submit/

    Encapsulates all form field interactions. Test file only calls
    fill_form() and submit_form() – no locators appear in test code.
    """

    # Locators for all form fields – class-level constants
    FIRST_NAME = (By.CSS_SELECTOR, "input[name='name']")
    EMAIL = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    COMPANY = (By.CSS_SELECTOR, "input[name='company']")
    WEBSITE = (By.CSS_SELECTOR, "input[name='websiteName']")
    COUNTRY_DROPDOWN = (By.CSS_SELECTOR, "select[name='country']")
    CITY = (By.CSS_SELECTOR, "input[name='city']")
    ADDRESS1 = (By.CSS_SELECTOR, "input[name='address_line1']")
    ADDRESS2 = (By.CSS_SELECTOR, "input[name='address_line2']")
    STATE = (By.CSS_SELECTOR, "input[name='state']")
    ZIP_CODE = (By.CSS_SELECTOR, "input[name='zip_code']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg")

    def fill_form(self, name, email, phone="1234567890", address="123 Test Street"):
        """
        Fill out the input form with the provided values.
        Phone maps to ZIP code since the form uses zip as contact number field.
        """
        from selenium.webdriver.support.ui import Select

        # Fill in First Name
        name_field = self.wait_for_element(self.FIRST_NAME)
        name_field.clear()
        name_field.send_keys(name)

        # Fill in Email
        email_field = self.wait_for_element(self.EMAIL)
        email_field.clear()
        email_field.send_keys(email)

        # Fill in Password (required field)
        pwd_field = self.wait_for_element(self.PASSWORD)
        pwd_field.clear()
        pwd_field.send_keys("TestPass123")

        # Fill in Company
        company_field = self.wait_for_element(self.COMPANY)
        company_field.clear()
        company_field.send_keys("Test Company")

        # Fill in Website
        website_field = self.wait_for_element(self.WEBSITE)
        website_field.clear()
        website_field.send_keys("https://testsite.com")

        # Select Country from dropdown
        country_select_el = self.wait_for_element(self.COUNTRY_DROPDOWN)
        country_select = Select(country_select_el)
        country_select.select_by_visible_text("United States")

        # Fill City
        city_field = self.wait_for_element(self.CITY)
        city_field.clear()
        city_field.send_keys("Test City")

        # Fill Address Line 1
        addr1_field = self.wait_for_element(self.ADDRESS1)
        addr1_field.clear()
        addr1_field.send_keys(address)

        # Fill Address Line 2
        addr2_field = self.wait_for_element(self.ADDRESS2)
        addr2_field.clear()
        addr2_field.send_keys("Suite 100")

        # Fill State
        state_field = self.wait_for_element(self.STATE)
        state_field.clear()
        state_field.send_keys("CA")

        # Fill ZIP code (used as phone in this form)
        zip_field = self.wait_for_element(self.ZIP_CODE)
        zip_field.clear()
        zip_field.send_keys("90001")

    def submit_form(self):
        """Click the form Submit button."""
        submit_btn = self.wait_for_element_clickable(self.SUBMIT_BUTTON)
        submit_btn.click()

    def get_success_message(self):
        """Wait for and return the success message text after form submission."""
        # Give the page a moment to process and show the message
        success_el = self.wait_for_element(self.SUCCESS_MESSAGE)
        return success_el.text
