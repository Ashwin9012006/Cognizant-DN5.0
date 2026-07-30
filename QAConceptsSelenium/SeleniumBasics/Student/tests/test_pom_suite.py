"""
Hands-On 7 – tests/test_pom_suite.py
Full POM-based test suite. Zero driver.find_element calls in this file.

Steps covered:
55. test_simple_form_submission using SimpleFormPage
56. test_checkbox_demo using CheckboxPage; test_dropdown_selection using DropdownPage
57. test_input_form_submit using InputFormPage
58. Run: pytest tests/ -v --html=report.html
59. POM maintenance comment at the bottom

WHY POM MATTERS – MAINTENANCE EXAMPLE:
If the Submit button's ID changes from 'showInput' to 'btn-submit' in a flat (non-POM) script:
  - You'd have to search through EVERY test file for 'showInput' and update it manually
  - One miss means a test that silently fails or throws NoSuchElementException
  - With POM: you update one line in simple_form_page.py (SUBMIT_BUTTON locator)
    and ALL tests that use SimpleFormPage automatically get the fix. Zero hunting.

This is the core benefit of POM: when the UI changes, only the page class changes,
not the tests. Tests become stable business logic, not brittle HTML interaction code.
"""

import sys
import os

# Add the parent directory to path so we can import from automation_scripts/pages/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'automation_scripts'))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# Step 55: Refactored test using SimpleFormPage – zero driver.find_element calls
def test_simple_form_submission(driver, base_url):
    """
    Test the Simple Form Demo using POM.
    This test reads like a business requirement, not HTML interaction code.
    """
    # Instantiate the page object with the driver
    page = SimpleFormPage(driver)

    # Navigate to the Simple Form Demo
    page.navigate_to(base_url + "simple-form-demo/")

    # Use page methods – no find_element calls here
    page.enter_message("Hello Selenium")
    page.click_submit()

    # Assert using the page method that returns the value
    actual_message = page.get_displayed_message()
    assert actual_message == "Hello Selenium", (
        f"Expected 'Hello Selenium', got '{actual_message}'"
    )


# Step 56: Refactored checkbox test using CheckboxPage
def test_checkbox_demo(driver, base_url):
    """Test checkbox interaction using CheckboxPage POM."""
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")

    # Click the first checkbox (index 0) – should be checked
    page.click_checkbox(0)
    assert page.is_option_checked(0), "Checkbox should be checked after first click"

    # Click again – should be unchecked
    page.click_checkbox(0)
    assert not page.is_option_checked(0), "Checkbox should be unchecked after second click"


# Step 56: Refactored dropdown test using DropdownPage
def test_dropdown_selection(driver, base_url):
    """Test dropdown selection using DropdownPage POM."""
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-list-demo/")

    # Select Wednesday using the page method
    page.select_day("Wednesday")

    # Assert using the page method
    selected = page.get_selected_day()
    assert selected == "Wednesday", f"Expected 'Wednesday', got '{selected}'"


# Step 57: New test using InputFormPage
def test_input_form_submit(driver, base_url):
    """
    Test the Input Form Submit page using InputFormPage POM.
    fill_form() and submit_form() encapsulate all form interactions.
    """
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-submit/")

    # Fill all required fields using the page method
    page.fill_form(
        name="John Doe",
        email="john.doe@test.com",
        phone="9876543210",
        address="456 Automation Avenue"
    )

    # Submit the form
    page.submit_form()

    # Get the success message and verify the form submitted successfully
    success_msg = page.get_success_message()
    assert success_msg is not None and len(success_msg) > 0, (
        "Expected a success message after form submission but got none"
    )
    print(f"Form submitted successfully. Message: {success_msg}")


"""
=== STEP 59: POM MAINTENANCE COMMENT ===

PROBLEM IN A FLAT (NON-POM) SCRIPT:
------------------------------------
If the Submit button's ID changes from 'showInput' to 'btn-submit':

In a flat script you might have 10 test functions all doing:
    driver.find_element(By.ID, "showInput").click()

You'd have to:
1. Search every test file for "showInput" (grep or find-replace)
2. Update each occurrence manually
3. Miss one → silent test failure that's hard to debug
4. If different tests have slightly different versions (some use CSS selector,
   some use XPath), you'd miss even more

With POM:
---------
Only ONE line changes in simple_form_page.py:
    SUBMIT_BUTTON = (By.ID, "btn-submit")   # was "showInput"

That's it. All 10 tests that use SimpleFormPage.click_submit() automatically
use the updated locator. No test file changes needed. No search-and-replace.
No possibility of missing an occurrence.

This is exactly why POM is the single most important design pattern in Selenium:
"Test files contain assertions (what should happen).
Page files contain interactions (how to make it happen)."
"""
