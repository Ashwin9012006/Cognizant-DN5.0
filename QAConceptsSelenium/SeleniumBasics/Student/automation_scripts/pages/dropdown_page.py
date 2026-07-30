"""
Hands-On 7 – pages/dropdown_page.py
Page Object for the Select Dropdown List Demo page.

Step 54: select_day() method using Select class internally
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class DropdownPage(BasePage):
    """
    Page Object for: https://www.lambdatest.com/selenium-playground/select-dropdown-list-demo/

    Uses the Selenium Select class internally to interact with the <select> element.
    The test file doesn't need to know about Select – it just calls select_day().
    """

    # Locator for the day-of-week dropdown
    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        """
        Select a day from the dropdown by its visible text (e.g., 'Wednesday').
        Uses Select class internally – the test file doesn't need to import Select.
        """
        # Wait for the dropdown to be present before interacting
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text(day_name)

    def get_selected_day(self):
        """Return the currently selected day's text."""
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        dropdown = Select(dropdown_element)
        return dropdown.first_selected_option.text

    def get_all_options(self):
        """Return a list of all available option texts in the dropdown."""
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        dropdown = Select(dropdown_element)
        return [option.text for option in dropdown.options]
