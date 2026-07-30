"""
Hands-On 7 – pages/checkbox_page.py
Page Object for the Checkbox Demo page.

Step 53: Methods for check/uncheck/verify by index
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckboxPage(BasePage):
    """
    Page Object for: https://www.lambdatest.com/selenium-playground/checkbox-demo/

    No assertions in this class. Only actions and state queries.
    """

    # The main single checkbox (used in basic demo section)
    SINGLE_CHECKBOX = (By.ID, "isAgeSelected")

    # Multiple checkboxes in the "Multiple Checkboxes" section
    # These are found dynamically by index since they don't have unique IDs
    CHECKBOX_CONTAINER = (By.CSS_SELECTOR, ".checkbox-demo")

    def _get_checkboxes(self):
        """Internal helper to get all checkbox input elements on the page."""
        return self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

    def check_option(self, index=0):
        """
        Check the checkbox at the given index (0-based).
        Only checks it if it's not already checked.
        """
        checkboxes = self._get_checkboxes()
        if index < len(checkboxes):
            if not checkboxes[index].is_selected():
                checkboxes[index].click()
        else:
            raise IndexError(f"No checkbox at index {index}. Found {len(checkboxes)} total.")

    def uncheck_option(self, index=0):
        """
        Uncheck the checkbox at the given index.
        Only unchecks if it's currently checked.
        """
        checkboxes = self._get_checkboxes()
        if index < len(checkboxes):
            if checkboxes[index].is_selected():
                checkboxes[index].click()
        else:
            raise IndexError(f"No checkbox at index {index}. Found {len(checkboxes)} total.")

    def is_option_checked(self, index=0):
        """Return True if the checkbox at the given index is selected, False otherwise."""
        checkboxes = self._get_checkboxes()
        if index < len(checkboxes):
            return checkboxes[index].is_selected()
        raise IndexError(f"No checkbox at index {index}. Found {len(checkboxes)} total.")

    def click_checkbox(self, index=0):
        """Click the checkbox at the given index regardless of its current state."""
        checkboxes = self._get_checkboxes()
        if index < len(checkboxes):
            checkboxes[index].click()
        else:
            raise IndexError(f"No checkbox at index {index}. Found {len(checkboxes)} total.")

    def get_single_checkbox(self):
        """Get the main single checkbox element (the primary one in the demo)."""
        return self.wait_for_element(self.SINGLE_CHECKBOX)
