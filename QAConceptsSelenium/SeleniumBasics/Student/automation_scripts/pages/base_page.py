"""
Hands-On 7 – pages/base_page.py
BasePage class – parent for all Page Object classes.

Step 50: Create BasePage with navigate_to(), get_title(), wait_for_element()
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Base class for all page objects. Provides common utilities like navigation
    and waiting for elements. Every page class inherits from this.
    """

    def __init__(self, driver):
        # Store the driver so all child page classes can use it
        self.driver = driver
        # Default wait timeout – overridable per element if needed
        self.wait_timeout = 15

    def navigate_to(self, url):
        """Navigate the browser to the given URL."""
        self.driver.get(url)

    def get_title(self):
        """Return the current page title."""
        return self.driver.title

    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be visible and return it.
        locator is a tuple: (By.ID, 'element-id')
        """
        if timeout is None:
            timeout = self.wait_timeout

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for an element to be clickable and return it."""
        if timeout is None:
            timeout = self.wait_timeout

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
