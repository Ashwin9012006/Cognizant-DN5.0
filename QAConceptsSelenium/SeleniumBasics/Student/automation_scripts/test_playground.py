"""
Hands-On 6 – test_playground.py
pytest test file for Selenium Playground automation.

Steps covered:
40. Renamed functions to start with test_
41. Tests receive driver via fixture injection (defined in conftest.py)
42. test_simple_form_submission - form input and assertion
43. test_checkbox_demo - checkbox click and state verification
44. Run with: pytest test_playground.py -v
45. Parameterized form submission test with 3 inputs
47. HTML report: pytest test_playground.py --html=report.html --self-contained-html
48. base_url fixture from conftest.py
49. test_dropdown_selection using Select class
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# Step 42: Test for Simple Form Demo
# - Opens the page using base_url fixture
# - Types a message, clicks Submit, waits for result, asserts text
def test_simple_form_submission(driver, base_url):
    # Navigate to the Simple Form Demo page
    driver.get(base_url + "simple-form-demo/")

    wait = WebDriverWait(driver, 15)

    # Wait for the message input field to appear and type into it
    message_input = wait.until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )
    message_input.clear()
    message_input.send_keys("Hello Selenium")

    # Click the Submit button
    submit_btn = driver.find_element(By.ID, "showInput")
    submit_btn.click()

    # Wait for the displayed message to appear in the result area
    displayed_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    # Assert the displayed text matches what we typed
    actual_text = displayed_msg.text
    assert actual_text == "Hello Selenium", (
        f"Expected 'Hello Selenium' but got '{actual_text}'"
    )


# Step 43: Test for Checkbox Demo
# - Clicks first checkbox, asserts selected
# - Clicks again, asserts deselected
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")

    wait = WebDriverWait(driver, 15)

    # Wait for the first checkbox to be present
    first_checkbox = wait.until(
        EC.presence_of_element_located((By.ID, "isAgeSelected"))
    )

    # Click it – should now be selected (checked)
    first_checkbox.click()
    assert first_checkbox.is_selected(), "Expected checkbox to be checked after first click"

    # Click again – should now be deselected (unchecked)
    first_checkbox.click()
    assert not first_checkbox.is_selected(), "Expected checkbox to be unchecked after second click"


# Step 45: Parameterized test – runs 3 times with different input values
# Each set of parameters creates a separate test entry in the report
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_parametrized(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")

    wait = WebDriverWait(driver, 15)

    # Clear any existing text and type the parameterized message
    message_input = wait.until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )
    message_input.clear()
    message_input.send_keys(message)

    # Submit the form
    submit_btn = driver.find_element(By.ID, "showInput")
    submit_btn.click()

    # Wait for and assert the displayed message
    displayed_msg = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    actual_text = displayed_msg.text
    assert actual_text == message, (
        f"Expected '{message}' but got '{actual_text}'"
    )


# Step 49: Dropdown selection test using the Select class
# from selenium.webdriver.support.ui import Select is the correct way to
# interact with <select> HTML elements – clicking options directly can be
# unreliable. The Select class handles the dropdown interaction properly.
def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-list-demo/")

    wait = WebDriverWait(driver, 15)

    # Wait for the select element to be present
    dropdown_element = wait.until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )

    # Wrap it with the Select class for proper dropdown interaction
    dropdown = Select(dropdown_element)

    # Select 'Wednesday' by its visible text
    dropdown.select_by_visible_text("Wednesday")

    # Assert the selected option text is 'Wednesday'
    selected_option = dropdown.first_selected_option
    assert selected_option.text == "Wednesday", (
        f"Expected 'Wednesday' to be selected but got '{selected_option.text}'"
    )
