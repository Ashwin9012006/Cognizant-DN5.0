"""
Hands-On 7 – tests/conftest.py
Shared fixtures for the POM test suite.

This is a copy of conftest.py for the tests/ directory so pytest discovers
it when running from the tests/ folder.
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """Session-scoped base URL – shared across all tests."""
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    """
    Function-scoped driver – each test gets a fresh browser instance.
    Setup runs before yield; teardown runs after yield.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)

    yield chrome_driver

    chrome_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            test_name = item.name.replace("/", "_").replace("[", "_").replace("]", "_")
            screenshot_path = os.path.join(screenshots_dir, f"{test_name}_failure.png")
            driver_fixture.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
