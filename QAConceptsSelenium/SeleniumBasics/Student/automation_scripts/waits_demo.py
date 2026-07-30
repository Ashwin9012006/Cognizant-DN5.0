"""
Hands-On 5 – Task 2: WebDriverWait and Expected Conditions

Steps covered:
36. Click Bootstrap Alert button, wait for alert div, assert text
37. Compare time.sleep() vs explicit wait with timing
38. Use EC.element_to_be_clickable(), explain difference from visibility
39. Use FluentWait with polling and NoSuchElementException ignore
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as FluentWait
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    """Helper to create a fresh Chrome driver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 800)
    return driver


def test_with_sleep():
    """Step 37 (Part 1): The bad way – using time.sleep(3)."""
    driver = get_driver()

    try:
        driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo/")
        time.sleep(2)  # wait for page load

        # Click the "Success Message" button
        success_btn = driver.find_element(By.CSS_SELECTOR, ".btn-success-manual")
        success_btn.click()

        start_time = time.monotonic()
        # Fixed sleep – always waits 3 seconds even if the alert appeared in 0.3 seconds
        time.sleep(3)
        end_time = time.monotonic()

        # Try to get the alert text
        alert = driver.find_element(By.CSS_SELECTOR, ".alert-success-manual")
        print(f"[SLEEP] Alert text: {alert.text}")
        print(f"[SLEEP] Time waited: {end_time - start_time:.2f} seconds")
        # Problem: we always wait 3s even when the element appears in 300ms
        # On slow networks, 3s might not even be enough and the test fails

    finally:
        driver.quit()


def test_with_explicit_wait():
    """Step 36 + Step 37 (Part 2): The correct way – using WebDriverWait."""
    driver = get_driver()

    try:
        # Step 36: Bootstrap Alerts demo with explicit wait
        driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo/")

        # Wait for page to be loaded – the button should be clickable before we use it
        wait = WebDriverWait(driver, 15)
        time.sleep(2)  # minimal page load wait for initial render

        # Click the "Success Message" button
        success_btn = driver.find_element(By.CSS_SELECTOR, ".btn-success-manual")
        success_btn.click()

        # Step 37: Time how long the explicit wait actually takes
        start_time = time.monotonic()

        # Wait for the success alert div to become visible (up to 10 seconds)
        # This returns as SOON as the condition is true, not after a fixed wait
        alert_element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success-manual"))
        )
        end_time = time.monotonic()

        # Assert the alert text contains 'successfully' or matches normal success text
        alert_text = alert_element.text
        assert "success" in alert_text.lower(), (
            f"Expected 'success' in alert text, got: {alert_text}"
        )
        print(f"[EXPLICIT WAIT] Alert text: {alert_text}")
        print(f"[EXPLICIT WAIT] Time waited: {end_time - start_time:.2f} seconds")
        # On fast machines this is much less than 3 seconds!
        # On slow machines, it waits longer than 3 seconds if needed.
        # This is why explicit wait is both faster AND more reliable.

    finally:
        driver.quit()


def test_element_to_be_clickable():
    """Step 38: Demonstrate EC.element_to_be_clickable()."""

    # EXPLANATION OF WAIT TYPES:
    # visibility_of_element_located: The element is present in the DOM AND visible
    # on the page (CSS display != 'none', opacity > 0, size > 0). But it could still
    # be disabled or have another element overlapping it (like a loading spinner).
    #
    # element_to_be_clickable: Extends visibility check – the element must also be
    # ENABLED (not disabled) and not covered by another element. Use this before
    # clicking buttons to avoid ElementClickInterceptedException or clicking a
    # disabled button that looks visible.

    driver = get_driver()

    try:
        driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo/")

        wait = WebDriverWait(driver, 15)

        # Wait for the button to be clickable (visible + enabled + not covered)
        # This is safer than just finding the element directly
        success_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success-manual"))
        )
        time.sleep(1) # Ensure page handlers are fully bound
        success_btn.click()
        print("[CLICKABLE WAIT] Button was confirmed clickable before clicking")

        # Now wait for the alert to be visible
        alert = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success-manual"))
        )
        print(f"[CLICKABLE WAIT] Alert appeared: {alert.text}")

    finally:
        driver.quit()


def test_fluent_wait():
    """
    Step 39: FluentWait – poll every 500ms, max 10 seconds,
    ignore NoSuchElementException during polling.

    FluentWait is more configurable than WebDriverWait – you can set:
    - poll_frequency: how often to check the condition
    - ignored_exceptions: exceptions to silently ignore during polling

    This is useful when waiting for dynamically loaded content that
    appears asynchronously (e.g., after an AJAX call or animation).
    """
    driver = get_driver()

    try:
        # We'll wait for a table row on the Table Sort page
        driver.get("https://www.lambdatest.com/selenium-playground/table-sort-search-demo/")

        # Configure FluentWait: check every 500ms, give up after 10 seconds,
        # and don't crash if the element is briefly not in the DOM during polling
        fluent_wait = FluentWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )

        # Wait for the first table row to appear and get its text inside the wait
        first_row_text = fluent_wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "#example tbody tr").text
        )
        print(f"[FLUENT WAIT] First table row found: {first_row_text[:80]}...")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("=== Test 1: time.sleep() approach (the bad way) ===")
    test_with_sleep()

    print("\n=== Test 2: Explicit WebDriverWait approach (the right way) ===")
    test_with_explicit_wait()

    print("\n=== Test 3: element_to_be_clickable() ===")
    test_element_to_be_clickable()

    print("\n=== Test 4: FluentWait with polling ===")
    test_fluent_wait()
