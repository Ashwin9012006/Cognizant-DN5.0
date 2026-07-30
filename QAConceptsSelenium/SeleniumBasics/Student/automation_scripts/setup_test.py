"""
Hands-On 4 – Task 1: Selenium Architecture and Environment Setup

Steps covered:
24. Describe Selenium components in comment block
25. Minimal script using webdriver-manager to open LambdaTest playground
26. Add implicit wait and explain why it's bad practice
27. Run in headless mode using ChromeOptions
"""

"""
=============================================================
SELENIUM ARCHITECTURE – THREE MAIN COMPONENTS
=============================================================

1. WebDriver
   WebDriver is the core component that acts as a bridge between
   your Python test code and the actual browser. It communicates
   with the browser using the W3C WebDriver protocol (a standardized
   HTTP-based protocol). Each browser has its own driver executable
   (ChromeDriver for Chrome, GeckoDriver for Firefox). When you call
   driver.get("https://example.com"), Python sends a command to
   ChromeDriver, which then instructs Chrome to navigate. The
   communication is bidirectional – the browser reports back element
   properties, page state, and screenshots.

2. Selenium Grid
   Selenium Grid solves the problem of running tests in parallel across
   multiple machines and multiple browser types. Without Grid, you can
   only test one browser on one machine at a time. Grid has a Hub (the
   central coordinator) and Nodes (machines with different browser
   setups). When you run tests against the Hub, it distributes them
   across available Nodes. This dramatically reduces overall test
   execution time for large test suites (e.g., running 100 tests across
   5 machines takes ~1/5 the time).

3. Selenium IDE
   Selenium IDE is a browser extension (available for Chrome and Firefox)
   used for record-and-playback automation. It records your manual
   browser interactions and generates test scripts in multiple languages
   (Python, Java, JavaScript). It's useful for quickly generating test
   scripts for simple scenarios and for non-developers who need to create
   basic automation without coding. However, generated scripts often
   need cleanup and are not production-quality.
=============================================================
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def run_setup_test():
    # Task 25: Set up driver using webdriver-manager
    # webdriver-manager automatically downloads the right ChromeDriver
    # version so we don't have to manage driver files manually
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Task 26: Adding implicit wait
    # implicit_wait tells the driver to wait up to N seconds before
    # throwing NoSuchElementException when looking for elements.
    # BUT this is considered bad practice for a few reasons:
    # - It applies globally to every single find_element() call
    # - It can interact unpredictably with explicit waits (using both together
    #   can cause double-wait time in some Selenium versions)
    # - It slows down tests that intentionally check for elements that
    #   DON'T exist (the driver waits the full timeout before confirming absence)
    # - Explicit waits are more precise – they wait for a SPECIFIC condition
    #   (visible, clickable, present) rather than just "in DOM or not"
    # Best practice: use explicit WebDriverWait with ExpectedConditions instead
    driver.implicitly_wait(10)

    try:
        # Navigate to the LambdaTest Selenium Playground
        driver.get("https://www.lambdatest.com/selenium-playground/")

        # Print the page title to confirm we loaded the right page
        page_title = driver.title
        print(f"Page title: {page_title}")

        # Give it a moment so we can see the browser if not headless
        time.sleep(2)

    finally:
        # Always quit the driver to close the browser and free resources
        driver.quit()
        print("Browser closed successfully.")


def run_headless_test():
    # Task 27: Run in headless mode using ChromeOptions
    # Headless mode means the browser runs without opening a visible window.
    # Useful for CI/CD pipelines where there is no display server (like Linux servers).
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")           # no visible browser window
    options.add_argument("--no-sandbox")         # required in some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # prevents crashes in Docker

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.lambdatest.com/selenium-playground/")

        # Title should still be fetched even without a visible window
        page_title = driver.title
        print(f"[Headless] Page title: {page_title}")

        # Confirm headless still works by checking URL
        print(f"[Headless] Current URL: {driver.current_url}")

    finally:
        driver.quit()
        print("[Headless] Browser closed.")


if __name__ == "__main__":
    print("=== Running normal (visible) browser test ===")
    run_setup_test()

    print("\n=== Running headless browser test ===")
    run_headless_test()
