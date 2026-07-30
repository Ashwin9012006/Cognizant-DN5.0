"""
Hands-On 4 – Task 2: WebDriver Navigation and Window Commands

Steps covered:
28. Navigate to Simple Form Demo, assert URL, go back
29. Open new tab, list handles, switch to new tab, print title
30. Switch back, take screenshot
31. get_window_size() and set_window_size()
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def run_navigation_test():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Task 31: Set a consistent window size before starting
    # Consistent window size matters for responsive UI automation because:
    # - Responsive websites show different layouts at different screen widths
    # - An element visible at 1920px might be hidden or moved in a mobile layout
    # - Without a fixed size, the same test might pass on a developer's wide monitor
    #   but fail on a CI server with a smaller virtual display
    # - Setting a fixed size ensures every test run sees the exact same page layout
    driver.set_window_size(1280, 800)

    # Show the current window size before we changed it
    size_before = driver.get_window_size()
    print(f"Window size set to: {size_before['width']}x{size_before['height']}")

    try:
        # Step 28: Open Selenium Playground and navigate to Simple Form Demo
        playground_url = "https://www.lambdatest.com/selenium-playground/"
        driver.get(playground_url)
        print(f"Opened: {driver.current_url}")

        # Wait for the Simple Form Demo link and click it
        wait = WebDriverWait(driver, 15)
        simple_form_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Simple Form Demo"))
        )
        simple_form_link.click()

        # Give the page a moment to load after the click
        time.sleep(2)

        # Assert the URL contains 'simple-form-demo'
        assert "simple-form-demo" in driver.current_url, (
            f"Expected 'simple-form-demo' in URL but got: {driver.current_url}"
        )
        print(f"URL assertion passed: {driver.current_url}")

        # Navigate back to the playground using driver.back()
        driver.back()
        time.sleep(1)
        print(f"After back(): {driver.current_url}")

        # Step 29: Open a new tab using JavaScript
        driver.execute_script('window.open("https://www.google.com");')
        time.sleep(1)

        # List all open window handles
        all_handles = driver.window_handles
        print(f"Number of open tabs: {len(all_handles)}")
        print(f"All window handles: {all_handles}")

        # Switch to the new tab (second handle in the list)
        driver.switch_to.window(all_handles[1])
        time.sleep(2)

        # Print the title of the Google tab
        google_title = driver.title
        print(f"New tab title (Google): {google_title}")

        # Step 30: Switch back to the original tab
        driver.switch_to.window(all_handles[0])
        time.sleep(1)
        print(f"Switched back to: {driver.title}")

        # Take a screenshot of the original tab
        screenshot_path = "playground_screenshot.png"
        driver.save_screenshot(screenshot_path)

        # Verify the screenshot file was actually created
        if os.path.exists(screenshot_path):
            file_size = os.path.getsize(screenshot_path)
            print(f"Screenshot saved: {screenshot_path} ({file_size} bytes)")
        else:
            print("ERROR: Screenshot file was not created!")

        # Step 31: Check and demonstrate window size methods
        current_size = driver.get_window_size()
        print(f"Current window size: {current_size['width']}x{current_size['height']}")

        # Change to a different size and confirm
        driver.set_window_size(1440, 900)
        new_size = driver.get_window_size()
        print(f"After resize: {new_size['width']}x{new_size['height']}")

    finally:
        driver.quit()
        print("All windows closed.")


if __name__ == "__main__":
    run_navigation_test()
