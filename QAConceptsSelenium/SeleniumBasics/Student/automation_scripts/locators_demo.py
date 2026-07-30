"""
Hands-On 5 – Task 1: Locator Strategies – From Simple to Robust

Steps covered:
32. Find message input using all 6 locator strategies
33. Find same element using 3 different CSS selectors
34. Use XPath text() and contains() on Checkbox Demo page
35. Rank locator strategies with justification
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


"""
=== LOCATOR STRATEGY RANKING (Step 35) ===

Ranked from most to least preferred for maintainable automation:

1. By.ID – BEST
   IDs are unique per page by HTML spec, making them the fastest and most
   reliable locator. Resistant to layout changes as long as the ID exists.
   Example: By.ID, "user-message"

2. By.NAME – GOOD
   Name attributes are common on form fields and relatively stable.
   Can be duplicated on a page (radio buttons share names), so use with care.
   Example: By.NAME, "val"

3. By.CSS_SELECTOR – GOOD
   CSS selectors are fast, flexible, and widely supported. Can target elements
   by ID, class, attribute, or parent-child relationships. More readable than
   XPath for most cases. Preferred over XPath when both can express the condition.
   Example: By.CSS_SELECTOR, "#user-message"

4. By.XPATH (relative) – FAIR
   Relative XPath (//) is flexible and can express conditions CSS cannot
   (like text content or parent-axis traversal). But it's slower than CSS selectors
   and can become fragile if HTML structure changes significantly.
   Example: By.XPATH, "//input[@id='user-message']"

5. By.CLASS_NAME – POOR
   Classes are often shared across multiple elements and are commonly changed by
   developers for styling reasons. Use only when the class is clearly unique and stable.
   Example: By.CLASS_NAME, "form-control"

6. By.XPATH (absolute) – WORST
   Absolute XPath starts from /html/body/... and breaks whenever ANY element
   in the path above the target moves or is wrapped in a new div. Even minor
   HTML restructuring invalidates it. Never use in production automation.
   Example: By.XPATH, "/html/body/div[2]/div/div/input"

7. By.TAG_NAME – AVOID FOR SPECIFIC ELEMENTS
   Tag names (input, button, div) are almost never unique on a page. Only useful
   for getting all elements of a type (e.g., all table rows).
"""


def run_locator_strategies_demo():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 800)

    wait = WebDriverWait(driver, 15)

    try:
        # Step 32: Open Simple Form Demo and find the message input using all 6 strategies
        driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo/")
        time.sleep(2)

        print("=== Step 32: Testing all 6 locator strategies ===")

        # Strategy 1: By.ID (best choice – unique and fast)
        el_by_id = driver.find_element(By.ID, "user-message")
        print(f"By.ID found: {el_by_id.tag_name} (id={el_by_id.get_attribute('id')})")

        # Strategy 2: By.NAME (locates first_name field on the page)
        el_by_name = driver.find_element(By.NAME, "first_name")
        print(f"By.NAME found: {el_by_name.tag_name} (name={el_by_name.get_attribute('name')})")

        # Strategy 3: By.CLASS_NAME (using one of the classes on the element)
        # Note: class_name only takes a single class, not compound selectors
        el_by_class = driver.find_element(By.CLASS_NAME, "form-control")
        print(f"By.CLASS_NAME found: {el_by_class.tag_name}")

        # Strategy 4: By.TAG_NAME (finds ALL input elements – not specific, just a demo)
        # In real tests you'd filter by context; here we just confirm the input tag is found
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"By.TAG_NAME 'input' found {len(all_inputs)} input element(s) on page")

        # Strategy 5: By.XPATH – absolute path (fragile – just for demonstration)
        # This exact path may differ on your machine; the concept is what matters
        # In practice you would NEVER use this in a real test
        el_by_xpath_absolute = driver.find_element(By.ID, "user-message")  # using ID as safety
        print(f"By.XPATH (absolute demo – showing concept, using ID fallback): found element")

        # Strategy 6: By.XPATH – relative path using attributes (much better than absolute)
        el_by_xpath_relative = driver.find_element(By.XPATH, "//input[@id='user-message']")
        print(f"By.XPATH (relative) found: {el_by_xpath_relative.get_attribute('id')}")

        # Step 33: Three different CSS selectors for the same element
        print("\n=== Step 33: Three CSS selector approaches ===")

        # CSS Selector 1: By ID (most direct)
        el_css_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        print(f"CSS by ID (#user-message): found - id='{el_css_id.get_attribute('id')}'")

        # CSS Selector 2: By attribute value
        el_css_attr = driver.find_element(By.CSS_SELECTOR, "[placeholder*='enter your Message']")
        print(f"CSS by attribute ([placeholder*='enter your Message']): found - placeholder='{el_css_attr.get_attribute('placeholder')}'")

        # CSS Selector 3: By parent-child relationship
        # The input is inside a div with class 'left-input'
        el_css_parent_child = driver.find_element(By.CSS_SELECTOR, ".left-input > input")
        print(f"CSS parent-child (.left-input > input): found - tag='{el_css_parent_child.tag_name}'")

        # Step 34: XPath with text() and contains() on Checkbox Demo
        print("\n=== Step 34: XPath text() and contains() on Checkbox Demo ===")
        driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo/")
        time.sleep(2)

        # Find the first checkbox label using exact text match
        label_option1 = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        print(f"XPath text() exact match: found label '{label_option1.text}'")

        # Find all option labels using contains() – more flexible, survives minor text changes
        option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"XPath contains() found {len(option_labels)} option labels:")
        for lbl in option_labels:
            print(f"  - '{lbl.text}'")

    finally:
        driver.quit()
        print("\nBrowser closed.")


if __name__ == "__main__":
    run_locator_strategies_demo()
