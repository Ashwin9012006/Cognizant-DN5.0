# SDLC vs TDLC – V-Model & Agile QA Integration

## Hands-On 2 – Written Exercise

---

## Task 1: V-Model Mapping

### 9. The V-Model Diagram

The V-Model maps each SDLC (development) phase on the left side to a corresponding TDLC (testing) phase on the right side, with Coding at the bottom vertex.

```
DEVELOPMENT SIDE                          TESTING SIDE
================                          ============

Requirements Analysis  <─────────────────> Acceptance Testing
       |                                        ^
       v                                        |
  System Design        <─────────────────> System Testing
       |                                        ^
       v                                        |
Architecture Design    <─────────────────> Integration Testing
       |                                        ^
       v                                        |
  Module Design        <─────────────────> Unit Testing
       |                                        ^
       v                                        |
              ──────────── CODING ────────────
                     (Bottom Vertex)
```

The V-Model shows that each left-side (development) phase has a corresponding right-side (testing) phase. Test planning happens during development, and actual testing happens after coding in parallel to how the system was built.

---

### 10. Test Artifacts Produced During Each Development Phase

| SDLC Phase | Corresponding Test Phase | Test Artifact Produced |
|---|---|---|
| Requirements Analysis | Acceptance Testing | Acceptance Test Plan – defines what the system must do from the user/business perspective. UAT scenarios are written from requirements. |
| System Design | System Testing | System Test Plan – test cases covering end-to-end flows, integration between all components, and complete business workflows. |
| Architecture Design | Integration Testing | Integration Test Plan – test cases for verifying how different modules/services communicate with each other (API contracts, data flows). |
| Module Design | Unit Testing | Unit Test Cases – test cases for individual functions and classes, based on detailed module specifications. |
| Coding | (Bottom vertex) | Test scripts are written and executed based on the test plans created in all previous phases. |

---

### 11. Entry & Exit Criteria for Each TDLC Phase

#### Unit Testing

**Entry Criteria:**
- Module design documents are complete and signed off
- Code for the module is written and compiled without errors
- Developer has conducted code review

**Exit Criteria:**
- All unit test cases have been executed
- Code coverage is at least 80%
- No open critical or high severity defects in unit tests
- All defects found are logged in the defect tracking system

---

#### Integration Testing

**Entry Criteria:**
- Unit testing is complete with all exit criteria met
- All modules to be integrated are available and stable
- Integration test plan and test cases are reviewed and approved
- Test environment is set up with all required services running

**Exit Criteria:**
- All integration test cases executed
- All API contracts verified
- No open critical defects related to module communication
- Defect count is below the agreed threshold

---

#### System Testing

**Entry Criteria:**
- Integration testing is complete with exit criteria met
- Complete system is deployed in the QA/staging environment
- System test plan is approved
- Test data is prepared for all test scenarios

**Exit Criteria:**
- All planned system test cases executed (typically 95%+)
- No open critical or high severity defects
- All major business workflows verified end-to-end
- Performance benchmarks are within acceptable limits
- Test summary report is reviewed and approved

---

#### Acceptance Testing (UAT)

**Entry Criteria:**
- System testing is complete with exit criteria met
- System is deployed in a UAT environment that mirrors production
- Business stakeholders and actual users are available for testing
- UAT test plan and acceptance criteria are signed off

**Exit Criteria:**
- All business-critical scenarios verified and approved by stakeholders
- No open P1/P2 defects
- User acceptance sign-off document is signed
- All identified defects are resolved or formally deferred
- Go/No-Go decision is made by the product owner

---

### 12. Two Places in the V-Model Where QA Should Engage Early

**Engagement Point 1 – Requirements Analysis Phase:**  
QA should participate in requirements reviews to check for ambiguities, missing acceptance criteria, and untestable requirements. For the Course Management API, this means reviewing whether `POST /api/courses/` requirements clearly define what happens with duplicate course codes, what the maximum allowed field lengths are, and what the exact HTTP status codes should be. Catching these gaps early prevents rework later.

**Engagement Point 2 – System Design / Architecture Phase:**  
QA should review the system design to identify testability risks – for example, if the architecture makes it hard to inject test data or if there are no logging mechanisms. For the Course Management API, QA would verify that the design includes proper error responses, database transaction handling, and that test environments can be set up independently.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems with Late Testing in Waterfall

**Problem 1 – Defects are discovered too late and cost too much to fix:**  
In waterfall, testing begins only after all development is done. For the Course Management API, if a fundamental design flaw in how courses handle duplicate codes is only discovered during the testing phase, it requires changes to the database schema, API logic, and possibly the frontend – all of which are expensive to rework at this stage.

**Problem 2 – No time to properly test because of schedule pressure:**  
Waterfall projects frequently run over on development time. Since testing is at the end, QA is the phase that gets squeezed when deadlines approach. The Course Management API might be rushed to production with inadequate testing because development took longer than planned.

**Problem 3 – Requirements misunderstandings are found too late:**  
In waterfall, requirements are frozen at the start. If the "create course" feature is built based on a misunderstood requirement – for example, QA assumes `course_code` must be unique globally, but developers assumed it only needs to be unique per department – this fundamental disagreement is only discovered during testing, wasting weeks of development work.

---

### 14. QA Role in Each Agile Ceremony

**Sprint Planning:**  
QA reviews the user stories selected for the sprint and helps write specific, testable acceptance criteria. For the Course Management API, QA would push to clarify exactly what success looks like for `POST /api/courses/`: "Given a valid course payload, when POST is called, then a 201 response is returned with the course ID." This makes the definition of done clear and prevents disagreements later.

**Daily Standup:**  
QA reports on testing progress and raises blockers that might affect the team. For example: "I'm blocked on testing the course creation endpoint because the database migration hasn't been applied to the QA environment yet. I need this resolved today to stay on track." This keeps the team aware of testing dependencies.

**Sprint Review:**  
QA participates in demonstrating completed features and may test features live during the demo. QA also provides input on whether the delivered functionality meets the acceptance criteria that were agreed on during sprint planning. For the API, QA might run a quick smoke test of all endpoints during the review.

**Retrospective:**  
QA shares observations about the testing process and suggests process improvements. For example: "We spent two days in this sprint retesting the same login bug three times because we don't have a clear regression test suite. I suggest we spend two hours in the next sprint creating automated smoke tests to catch regressions earlier."

---

### 15. Four Shift-Left Practices for Course Management API

**Practice (a) – Reviewing Requirements for Testability:**  
Before any code is written, QA reviews the requirements for `POST /api/courses/` to check: Are all required fields clearly specified? Is the behavior for invalid inputs defined? What are the exact HTTP status codes for each scenario? This ensures the API is designed with clear acceptance criteria that can be tested.

**Practice (b) – Writing Test Cases Before Code (TDD/BDD):**  
Using Test-Driven Development or Behavior-Driven Development, test cases for the Course Management API are written before the API code. For example, writing `test_create_course_returns_201_with_valid_data()` before the endpoint is implemented. The developer writes code to make this test pass, which naturally results in code that meets the requirement.

**Practice (c) – Static Code Analysis:**  
Automated tools like `flake8`, `pylint`, or `bandit` are integrated into the CI pipeline and run on every commit before tests even run. For the Course Management API, `bandit` would catch potential security issues like SQL injection vulnerabilities, and `pylint` would catch code quality issues before QA even sees the code.

**Practice (d) – API Contract Testing Before Integration:**  
Before different teams (or different services) integrate with the Course Management API, contract tests verify that the API's response format, status codes, and error messages match what the consumers expect. Tools like Pact can be used to define the expected API contract and verify both producer and consumer adhere to it, preventing integration failures from being discovered late.

---

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** "As a college admin, I want to create a new course, so that students can enroll in it."

---

**Scenario 1: Happy Path – Successful course creation**

```gherkin
Given I am logged in as a college admin
And there is no existing course with code "CS101"
When I send a POST request to /api/courses/ with the following data:
  | course_code   | CS101           |
  | course_name   | Intro to CS     |
  | credits       | 3               |
  | max_students  | 50              |
Then the API should return HTTP status 201 Created
And the response body should contain the course_id
And the response body should contain course_code "CS101"
And the new course should be retrievable via GET /api/courses/{course_id}
```

---

**Scenario 2: Duplicate Course Code**

```gherkin
Given I am logged in as a college admin
And a course with code "CS101" already exists in the system
When I send a POST request to /api/courses/ with course_code "CS101"
Then the API should return HTTP status 400 Bad Request
And the response body should contain an error message indicating "Course code already exists"
And no new course record should be created in the database
```

---

**Scenario 3: Missing Required Fields**

```gherkin
Given I am logged in as a college admin
When I send a POST request to /api/courses/ with only course_code "CS102" and no course_name
Then the API should return HTTP status 422 Unprocessable Entity
And the response body should contain a validation error for the "course_name" field
And the error message should clearly state which field is missing
And no course record should be created in the database
```
