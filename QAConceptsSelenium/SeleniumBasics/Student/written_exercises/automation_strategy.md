# Test Automation Process, Lifecycle & Framework Types

## Hands-On 3 – Written Exercise (Automation Strategy)

---

## Task 1: Automation Decision and Test Case Selection

### 17. Five Criteria for Deciding Whether to Automate

**Criterion 1 – Repeatability / Frequency of Execution:**  
Tests that are run many times (e.g., every sprint, every build) are great candidates for automation because the time investment pays off quickly. Tests that are run only once or rarely are poor candidates.  
*Applied to `POST /api/courses/` returning 201:* This is a core regression test that should run after every deployment. High repeatability → **Automate**.

**Criterion 2 – Stability of the Feature:**  
Tests for features that are stable and unlikely to change frequently are better candidates. Rapidly changing features lead to high maintenance costs in automation.  
*Applied to `POST /api/courses/`:* The basic contract of a REST endpoint (valid data → 201) is unlikely to change even as the feature evolves. Stable → **Automate**.

**Criterion 3 – Risk Level / Business Criticality:**  
High-risk areas (core business logic, authentication, payments) should always be automated to catch regressions quickly.  
*Applied to `POST /api/courses/`:* Course creation is a core business function. High risk → **Automate**.

**Criterion 4 – Complexity of Test Execution:**  
Tests requiring precise timing, large datasets, or complex setup are better automated. Tests requiring human judgment (e.g., "does this look right visually?") are better done manually.  
*Applied to `POST /api/courses/`:* API tests only require sending HTTP requests and checking responses – no human judgment needed. Well-suited for automation.

**Criterion 5 – Cost vs. Benefit (ROI Potential):**  
The automation effort must be justified by the time saved over multiple runs. Simple tests with high execution frequency have high ROI. Complex tests run rarely have low ROI.  
*Applied to `POST /api/courses/`:* Writing the test takes a few hours; running it takes seconds. If run 50+ times, the ROI is clearly positive → **Automate**.

---

### 18. Automate vs Manual Classification for Course Management API Test Cases

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | High frequency, repetitive, stable endpoints, zero judgment required – classic automation candidate |
| (b) Exploratory testing of a new search feature | **Manual** | Exploratory testing requires human creativity and judgment to discover unexpected behavior – automation cannot replace this |
| (c) Performance test: 100 concurrent users on GET /api/courses/ | **Automate** | Manual performance testing with 100 users is impossible; tools like locust or k6 make this straightforward |
| (d) UI test for the login form | **Automate** | High frequency, regression-critical, stable form – good Selenium candidate once the form is stable |
| (e) Verify API documentation (Swagger) is accurate | **Manual** | Requires human review and comparison of docs vs behavior; documentation checking involves judgment |
| (f) Smoke test: verify API is reachable after deployment | **Automate** | Should run automatically after every deployment as a health check; minimal effort, maximum value |

---

### 19. Test Automation ROI Calculation

**Definition of Automation ROI:**  
Return on Investment (ROI) for test automation is the point at which the time saved by running automated tests exceeds the time invested in creating and maintaining them. It answers: "Was it worth automating this test?"

**Scenario:**
- Time to automate one regression test: **4 hours**
- Time to run manually each time: **30 minutes (0.5 hours)**
- Maintenance overhead: **20% per run after the 10th run** (i.e., 0.20 × 0.5 = 0.1 hours per run)

**Break-even calculation (no maintenance yet):**
```
4 hours (investment) ÷ 0.5 hours (manual run) = 8 runs to break even (before maintenance)
```

**But with 20% maintenance after the 10th run:**  
After run 10, each run costs 20% of the manual time in maintenance = 0.5 × 0.2 = **0.1 hours extra per run**

- Runs 1-10: save 0.5h each = 5h saved total, investment = 4h. Net gain after 10 runs = +1h
- Runs 11+: each run saves 0.5h but costs 0.1h maintenance = net saving of 0.4h per run

The automation still pays off long-term. After 10 runs there is already a positive return, and every subsequent run continues to save time despite the maintenance overhead.

**Conclusion:** The break-even point is at **8 runs** (ignoring maintenance). With the 20% maintenance overhead starting after run 10, the net savings per run decrease slightly, but the automation remains profitable from run 8 onward.

---

### 20. Flaky Tests – Definition, Example, and Prevention

**What is a flaky test?**  
A flaky test is one that produces inconsistent results (sometimes passes, sometimes fails) without any change to the application code or test code. Flaky tests erode confidence in the test suite because failures cannot be trusted as real bugs.

**Example of a flaky Selenium test:**  
```python
# Flaky: uses a fixed sleep and assumes the page loads within 2 seconds
driver.get("https://example.com/courses")
time.sleep(2)  # what if the page takes 3 seconds on a slow network?
element = driver.find_element(By.ID, "course-list")
assert element.is_displayed()
```
This test will fail intermittently when the page takes longer than 2 seconds to load.

**Three Strategies to Prevent/Fix Flaky Tests:**

1. **Replace time.sleep() with Explicit Waits:**  
   Use `WebDriverWait` with `ExpectedConditions` instead of fixed sleeps. This waits up to a timeout for a specific condition to be true, rather than guessing how long to wait.
   ```python
   # Fixed: waits up to 10 seconds for the element to appear
   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "course-list")))
   ```

2. **Use Stable, Unique Locators:**  
   Avoid locators that depend on element position (`find_elements()[3]`) or auto-generated IDs that change on each page load. Prefer IDs, data-* attributes, or stable CSS selectors.

3. **Isolate Test Data:**  
   Ensure each test creates and cleans up its own data, rather than depending on shared test data that other tests might modify. Database state shared between tests causes intermittent failures depending on execution order.

---

## Task 2: Compare Automation Framework Types

### 21. Five Automation Framework Types

---

#### Linear (Record & Playback) Framework

**Description:**  
The simplest framework type – tests are written as a single, sequential script from top to bottom. Each test is self-contained with no shared code between tests. Often generated using record-and-playback tools like Selenium IDE.

**Advantage:** Very easy to get started with – no programming knowledge required. Good for quick one-off demos or very small projects.

**Disadvantage:** Highly non-maintainable at scale. If the login page changes, every single test script that includes login steps must be updated individually. Code duplication is extreme.

**Example for Course Management:**  
A single script that opens the browser, navigates to login, fills in credentials, navigates to courses, creates a course, and verifies it. Simple to write, but impossible to scale to 50 test cases without massive duplication.

---

#### Modular Framework

**Description:**  
Breaks the application into independent, reusable modules. Common functions (like login, logout, navigate to courses) are written once as reusable functions and called from multiple test scripts.

**Advantage:** Eliminates code duplication. If login flow changes, only the login module is updated, and all tests that use it automatically get the fix.

**Disadvantage:** Tests still need to be written per scenario; test data is hardcoded in the scripts. Does not scale well for data-driven scenarios.

**Example for Course Management:**  
A `login()` module, a `create_course()` module, and a `verify_course()` module. Test scripts call these modules in sequence. Login changes affect only the login module.

---

#### Data-Driven Framework

**Description:**  
Separates test logic from test data. The same test script runs multiple times with different sets of data read from external sources (Excel, CSV, JSON, database).

**Advantage:** A single test can cover dozens of input scenarios without duplicating code. Adding new test cases is as simple as adding a row to a spreadsheet.

**Disadvantage:** Requires setup for data management infrastructure. Can be complex to handle expected results for different input types.

**Example for Course Management:**  
A single `test_create_course()` script reads from a CSV file containing 50 rows of different course data (valid data, invalid data, edge cases). Each row becomes a separate test run.

---

#### Keyword-Driven Framework

**Description:**  
Tests are written as a sequence of keywords (e.g., `OpenBrowser`, `Login`, `ClickButton`, `VerifyText`) in a spreadsheet or table format. Non-technical team members can write tests by combining keywords without knowing how to code.

**Advantage:** Non-technical stakeholders (business analysts, product owners) can participate in writing tests. Clear separation of implementation from test design.

**Disadvantage:** Very complex to set up initially. The keyword library must be maintained by developers. Can become unwieldy for complex scenarios.

**Example for Course Management:**  
A test table reads: `OpenBrowser | Navigate | https://example.com/courses | Login | admin | password | ClickButton | Create Course`. The framework maps each keyword to a Python function behind the scenes.

---

#### Hybrid Framework

**Description:**  
Combines the best features of multiple framework types – typically Modular + Data-Driven + Page Object Model, and optionally Keyword-Driven. This is the most common framework type in real-world projects.

**Advantage:** Maximum reusability (modular), parameterisation (data-driven), maintainability (POM), and flexibility. Suits projects of any scale.

**Disadvantage:** Higher initial setup complexity. Requires strong architectural decisions upfront. Not ideal for very small projects where the overhead isn't worth it.

**Example for Course Management:**  
Page Object classes for each page (POM), parametrized test data from JSON files (data-driven), shared fixtures via conftest.py (modular). New test cases are just new data rows plus a test function calling page methods.

---

### 22. Framework Recommendation for Course Management Frontend

**Scenario requirements:**
- Test login with **50 different user/password combinations** → needs Data-Driven
- **Reuse login steps** across 20 test cases → needs Modular / POM
- Support both **technical and non-technical team members** writing tests → needs Keyword-Driven elements

**Recommendation: Hybrid Framework (Data-Driven + POM + Optional BDD)**

I would recommend a **Hybrid framework** combining:
- **Page Object Model** for all UI interactions (LoginPage, CoursePage, etc.) – ensures non-POM test files are readable
- **Data-Driven approach** using pytest's `@pytest.mark.parametrize` or external CSV/JSON files for the 50 login combinations
- **pytest + conftest.py** for shared fixtures (reusable login setup)
- **BDD (Behave)** optionally for the non-technical team members, since Gherkin feature files are readable without coding knowledge

This combination addresses all three requirements without overcomplicating the architecture.

---

### 23. Hybrid Framework Folder Structure for Course Management Frontend

```
CourseManagement_Tests/
│
├── config/
│   ├── config.ini              # Base URL, browser type, timeouts, environment settings
│   └── test_settings.py        # Python config loader
│
├── test_data/
│   ├── login_credentials.csv   # 50 user/password combinations for data-driven login tests
│   ├── course_data.json        # Course creation test data (valid, invalid, edge cases)
│   └── expected_results.json   # Expected API responses for verification
│
├── pages/                      # Page Object Model – one class per page
│   ├── base_page.py            # BasePage class with common methods (navigate, wait, etc.)
│   ├── login_page.py           # LoginPage – locators and actions for login screen
│   ├── course_list_page.py     # CourseListPage – course table, search, filters
│   └── create_course_page.py   # CreateCoursePage – form fields, submit button
│
├── utilities/
│   ├── driver_factory.py       # Creates WebDriver instances (Chrome/Firefox/headless)
│   ├── data_reader.py          # Reads test data from CSV/JSON files
│   ├── screenshot_util.py      # Captures screenshots on failure
│   └── logger.py               # Test execution logging
│
├── tests/
│   ├── conftest.py             # pytest fixtures (driver setup/teardown, base_url)
│   ├── test_login.py           # Login test cases (parametrized with 50 credentials)
│   ├── test_course_creation.py # Course creation tests using CreateCoursePage POM
│   └── test_course_list.py     # Course list, search, and filter tests
│
├── reports/
│   ├── report.html             # Generated by pytest-html
│   └── screenshots/            # Auto-captured on test failure
│
├── requirements.txt            # selenium, pytest, webdriver-manager, pytest-html
└── README.md                   # Setup instructions and test execution guide
```

**Why this structure?**
- `pages/` – POM ensures no locators appear in test files; single point of update when UI changes
- `test_data/` – Separates data from logic; non-technical members can add test cases by editing CSV/JSON
- `utilities/` – Shared infrastructure used across all tests without duplication
- `conftest.py` – Centralizes browser setup; all 20 test files reuse the same login fixture
- `reports/` – Auto-generated reports for stakeholders without technical knowledge
