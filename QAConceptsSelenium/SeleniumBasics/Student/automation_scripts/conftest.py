"""
Hands-On 6 – conftest.py
Shared fixtures for all pytest tests.

Contains:
- driver fixture (function scope – new browser per test)
- base_url fixture (session scope – shared URL constant)
- Screenshot on failure hook
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Session-scoped fixture – created once and shared across all tests (Step 48)
# base_url is a constant so we don't hardcode the URL in every test
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Function-scoped fixture – creates a new browser instance for each test (Step 41)
# scope='function' means every test gets its own fresh browser, fully isolated.
# scope='session' would reuse one browser for all tests (faster but tests can
# affect each other via leftover cookies, state, or page navigation).
@pytest.fixture(scope="function")
def driver():
    # Set up Chrome with options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)
    chrome_driver.implicitly_wait(5)

    # Yield gives the driver to the test (setup is done above yield)
    yield chrome_driver

    # Teardown runs after the test completes (equivalent to tearDown in unittest)
    chrome_driver.quit()


# Step 46: Screenshot on failure hook
# This hook runs after every test. If the test failed, we capture a screenshot.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Run the test and get the result
    outcome = yield
    report = outcome.get_result()

    # We only care about the "call" phase (not setup or teardown)
    if report.when == "call" and report.failed:
        # Try to get the driver from the test's fixtures
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            # Create a screenshots folder if it doesn't exist
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Build a safe filename from the test name
            test_name = item.name.replace("/", "_").replace("[", "_").replace("]", "_")
            screenshot_path = os.path.join(screenshots_dir, f"{test_name}_failure.png")

            driver_fixture.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved on failure: {screenshot_path}")
