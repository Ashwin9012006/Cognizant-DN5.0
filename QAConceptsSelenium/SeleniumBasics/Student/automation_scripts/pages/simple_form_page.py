"""
Hands-On 7 – pages/simple_form_page.py
Page Object for the Simple Form Demo page.

Step 51: Locators as class-level tuples (not inside methods)
Step 52: Action methods that perform interactions and return values (no assertions here)
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class SimpleFormPage(BasePage):
    """
    Page Object for: https://www.lambdatest.com/selenium-playground/simple-form-demo/

    Golden rule: This class only knows HOW to interact with the page.
    It never asserts anything. Assertions belong in the test files.

    Locators are class-level constants so that if the ID changes in the HTML,
    we only update ONE line in ONE file instead of searching through every test.
    """

    # Step 51: Locators defined as class-level tuples – never hardcoded inside methods
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        """Type text into the message input field."""
        # Wait for the input to be visible before interacting with it
        input_field = self.wait_for_element(self.MESSAGE_INPUT)
        input_field.clear()
        input_field.send_keys(text)

    def click_submit(self):
        """Click the Submit button."""
        # Wait for the button to be clickable before clicking
        submit_btn = self.wait_for_element_clickable(self.SUBMIT_BUTTON)
        submit_btn.click()

    def get_displayed_message(self):
        """Wait for the result message to appear and return its text."""
        # We wait for the message element to be visible after submission
        msg_element = self.wait_for_element(self.DISPLAYED_MESSAGE)
        return msg_element.text
