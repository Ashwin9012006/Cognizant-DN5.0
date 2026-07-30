# QA Concepts & Selenium Basics – Hands-On Exercises

**Digital Nurture 5.0 | Python Full Stack Engineer Track**

---

## Project Structure

```
SeleniumBasics/Student/
├── written_exercises/
│   ├── qa_concepts.md          # Hands-On 1: QA concepts, testing types, defect lifecycle
│   ├── v_model_analysis.md     # Hands-On 2: SDLC vs TDLC, V-Model, Agile QA
│   └── automation_strategy.md  # Hands-On 3: Automation process, ROI, framework types
│
├── automation_scripts/
│   ├── setup_test.py           # Hands-On 4, Task 1: Selenium setup, headless mode
│   ├── navigation_test.py      # Hands-On 4, Task 2: Navigation, tabs, screenshots
│   ├── locators_demo.py        # Hands-On 5, Task 1: All 6 locator strategies
│   ├── waits_demo.py           # Hands-On 5, Task 2: WebDriverWait, FluentWait
│   ├── conftest.py             # Hands-On 6: Shared pytest fixtures
│   ├── test_playground.py      # Hands-On 6: pytest tests with parametrize
│   └── pages/                  # Hands-On 7: Page Object Model classes
│       ├── __init__.py
│       ├── base_page.py
│       ├── simple_form_page.py
│       ├── checkbox_page.py
│       ├── dropdown_page.py
│       └── input_form_page.py
│
├── tests/
│   ├── conftest.py             # Fixtures for POM test suite
│   └── test_pom_suite.py       # Hands-On 7: Full POM-based test suite
│
├── requirements.txt
└── README.md
```

---

## Setup

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure Google Chrome is installed (latest version)
4. `webdriver-manager` handles ChromeDriver automatically

---

## Running the Tests

### Run Hands-On 4 scripts directly:
```bash
python automation_scripts/setup_test.py
python automation_scripts/navigation_test.py
```

### Run Hands-On 5 scripts:
```bash
python automation_scripts/locators_demo.py
python automation_scripts/waits_demo.py
```

### Run Hands-On 6 pytest tests:
```bash
cd automation_scripts
pytest test_playground.py -v
pytest test_playground.py -v --html=report.html --self-contained-html
```

### Run Hands-On 7 POM test suite:
```bash
pytest tests/ -v
pytest tests/ -v --html=report.html --self-contained-html
```

---

## Test Site
All automation targets: https://www.lambdatest.com/selenium-playground/
