# QA Concepts, Functional Testing & Defect Lifecycle

## Hands-On 1 – Written Exercise

---

## Task 1: Map Testing Types to a Real System

### 1. Test Cases for Each Testing Type (Course Management API)

**Unit Testing** – Test a single function in isolation  
- Test case: Verify that the `validate_course_code()` function returns `False` when the course code contains special characters. The database and API layer are not involved; only the function itself is called in isolation using mocked inputs.

**Integration Testing** – Test two components working together  
- Test case: Call `POST /api/courses/` with valid JSON data and verify that the record is actually saved in the database. This tests the API endpoint and database together – if either side has an issue, the test catches it.

**System Testing** – End-to-end flow from API request to database response  
- Test case: Submit a complete course creation request with all required fields, confirm the 201 response, then call `GET /api/courses/{id}` and verify the returned data matches what was submitted. This covers the full system flow.

**User Acceptance Testing** – Test from the perspective of the actual user  
- Test case: A college admin logs into the admin panel, fills out the "Create Course" form, clicks Submit, and verifies the new course appears in the course list. This simulates how a real user would interact with the system.

---

### 2. Functional vs Non-Functional Classification

| Test Case | Type | Reason |
|---|---|---|
| Unit test – validate_course_code() | Functional | Checks correctness of a specific function's behavior |
| Integration test – POST + DB | Functional | Checks that two components work correctly together |
| System test – full E2E flow | Functional | Verifies the system does what it's supposed to do |
| UAT – admin creates course | Functional | Validates behavior from a user's perspective |

**Non-Functional Example:**  
Performance test – Send 200 concurrent `GET /api/courses/` requests and verify average response time is under 500ms and no errors occur. This tests *how well* the system performs, not *what* it does.

---

### 3. Black-Box vs White-Box Testing

**Black-Box Testing:**  
The tester has no knowledge of the internal code. They only interact with inputs and outputs. For example, calling `POST /api/courses/` with different payloads and checking responses without knowing how the API is implemented internally.

**White-Box Testing:**  
The tester knows the internal code and can design tests to cover specific code paths, branches, and conditions. For example, looking at the course creation function and writing a test specifically for the `if course_code already exists` branch.

- **QA testers** typically perform **Black-Box Testing** – they test the system as a user would, based on requirements.
- **Developers** typically perform **White-Box Testing** – they write unit tests with direct knowledge of the code they wrote.

---

### 4. Formal Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-001 | Create a new course with all valid required fields | API is running; database is accessible; no course with code CS101 exists | 1. Send POST /api/courses/ with body: `{"course_code": "CS101", "course_name": "Intro to CS", "credits": 3}` 2. Check the HTTP status code 3. Check the response body | 201 Created; response body contains course_id, course_code: "CS101", course_name: "Intro to CS" | | |
| TC-002 | Create a course with a duplicate course code | Course CS101 already exists in the database | 1. Send POST /api/courses/ with body: `{"course_code": "CS101", "course_name": "Duplicate Course", "credits": 3}` 2. Check the HTTP status code 3. Check the response body | 400 Bad Request; response body contains error message indicating duplicate course code | | |
| TC-003 | Create a course with missing required fields (no course_name) | API is running; database is accessible | 1. Send POST /api/courses/ with body: `{"course_code": "CS102", "credits": 3}` (no course_name) 2. Check the HTTP status code 3. Check the response body | 422 Unprocessable Entity; response body lists validation error for missing course_name field | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Complete Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
```

**States explained:**

- **New** – Defect is logged by the tester but not yet reviewed
- **Assigned** – A developer is assigned to investigate the defect
- **Open** – Developer has acknowledged the defect and is actively working on it
- **Fixed** – Developer has made a code fix and marked the defect as resolved
- **Retest** – QA retests the fix in the same environment and build where it was found
- **Verified** – QA confirms the fix works correctly
- **Closed** – Defect is officially resolved and no longer active

**Alternate Paths:**

- **Rejected** – Developer reviews the defect and decides it is not a valid bug (e.g., works as designed or cannot be reproduced). It goes from Assigned/Open → Rejected. QA reviews and either accepts or reopens.
- **Deferred** – The defect is real but is intentionally postponed to a future release due to low priority or scope constraints. Goes from Assigned/Open → Deferred → (revisited in next release).
- **Reopened** – If a verified fix is found to still be broken, the defect is reopened and goes back to Assigned → Open.

---

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| a) POST /api/courses/ returns 500 for all requests | **Critical** | **P1** | Core functionality is completely broken. Users cannot create courses at all. Must be fixed immediately. |
| b) Course names > 150 chars are silently truncated | **High** | **P2** | Data integrity issue – user-entered data is lost without any warning. This could cause business logic errors but the API still works for most cases. |
| c) /docs Swagger page has a typo in the description | **Low** | **P4** | Only affects documentation, not functionality. No user workflows are impacted. Can be scheduled for a future maintenance release. |
| d) Login with correct credentials occasionally returns 401 on first attempt | **High** | **P1** | Intermittent login failures directly affect user experience and indicate deeper instability. Even though it's intermittent, authentication issues are critical for security and trust. |

---

### 7. Complete Defect Report for Bug (a)

| Field | Details |
|---|---|
| **Defect ID** | DEF-001 |
| **Title** | POST /api/courses/ returns 500 Internal Server Error for all requests |
| **Environment** | QA Environment – Local development server, Windows 10, Python 3.11, FastAPI 0.104.1 |
| **Build Version** | v1.2.0-beta (Build #45) |
| **Severity** | Critical |
| **Priority** | P1 |
| **Reported By** | QA Tester |
| **Date Reported** | 2024-01-15 |
| **Assigned To** | Backend Developer |
| **Steps to Reproduce** | 1. Start the API server with `uvicorn main:app --reload` 2. Open Postman or any REST client 3. Send a POST request to `http://localhost:8000/api/courses/` with valid JSON body: `{"course_code": "CS101", "course_name": "Intro to CS", "credits": 3, "max_students": 30}` 4. Observe the HTTP response |
| **Expected Result** | HTTP 201 Created response with the created course details in the response body |
| **Actual Result** | HTTP 500 Internal Server Error with response body: `{"detail": "Internal Server Error"}` |
| **Attachments** | Screenshot of 500 error response in Postman; Server logs showing stack trace |

---

### 8. Severity vs Priority – Key Difference

**Severity** measures the *technical impact* of a defect on the system – how much damage it causes to functionality.

**Priority** measures *how urgently* the defect needs to be fixed – based on business impact and deadlines.

**Real-world example where High Severity ≠ High Priority:**

> The application crashes when a user uploads a file larger than 2GB (High Severity – crashes the app), but this scenario applies only to internal data scientists who upload large datasets once a month. Meanwhile, a cosmetic bug where the company logo appears blurry on the main login page has Low Severity but High Priority because the CEO demo is tomorrow and the company brand image matters.

In this case, the logo bug gets fixed first (High Priority) even though the crash bug is more technically severe.
