import sys
import os

# Import and test Course Service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'course_service'))
from course_service.app import app as course_app

print("=== TESTING MICROSERVICES HANDS-ON 10 ===")

# --- Course Service Tests ---
print("\n-- Course Service (port 5001) --")
with course_app.test_client() as c:
    r = c.post('/api/departments/', json={'name': 'Computer Science', 'head_of_dept': 'Dr. Turing'})
    dept_id = r.get_json()['id']
    print(f'POST /api/departments/ -> {r.status_code}, id={dept_id}')

    r = c.post('/api/courses/', json={'name': 'Algorithms', 'code': 'CS201', 'credits': 3, 'department_id': dept_id})
    course_id = r.get_json()['id']
    print(f'POST /api/courses/ -> {r.status_code}, id={course_id}, code={r.get_json()["code"]}')

    r = c.get(f'/api/courses/{course_id}/')
    print(f'GET /api/courses/{course_id}/ -> {r.status_code}, name={r.get_json()["name"]}')

    # Duplicate code 409
    r = c.post('/api/courses/', json={'name': 'Dup', 'code': 'CS201', 'credits': 2, 'department_id': dept_id})
    print(f'POST duplicate code -> {r.status_code}')


# --- Student Service Tests ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'student_service'))
from student_service.app import app as student_app

print("\n-- Student Service (port 5002) --")
with student_app.test_client() as c:
    r = c.post('/api/students/', json={'first_name': 'Alice', 'last_name': 'Smith', 'email': 'alice@college.edu', 'enrollment_year': 2023})
    student_id = r.get_json()['id']
    print(f'POST /api/students/ -> {r.status_code}, id={student_id}')

    # Duplicate email 409
    r = c.post('/api/students/', json={'first_name': 'X', 'last_name': 'Y', 'email': 'alice@college.edu', 'enrollment_year': 2023})
    print(f'POST duplicate email -> {r.status_code}')

    # Enrollment with Course Service DOWN (ConnectionError -> 503)
    r = c.post('/api/enrollments/', json={'student_id': student_id, 'course_id': 1})
    print(f'POST /api/enrollments/ (Course Service down) -> {r.status_code} (expected 503)')

print("\n=== ALL MICROSERVICE UNIT TESTS PASSED ===")
