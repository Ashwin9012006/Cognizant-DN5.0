from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Seed department and course
dept = client.post('/api/departments/', json={'name': 'CS', 'head_of_dept': 'Dr. T', 'budget': 90000.0}).json()
course = client.post('/api/courses/', json={'name': 'Algorithms', 'code': 'CS201', 'credits': 3, 'department_id': dept['id']}).json()
student = client.post('/api/students/', json={'first_name': 'Alice', 'last_name': 'S', 'email': 'a@college.edu', 'department_id': dept['id'], 'enrollment_year': 2023}).json()

# Enrollment with background task
r = client.post('/api/enrollments/', json={'student_id': student['id'], 'course_id': course['id']})
print('POST /api/enrollments/ ->', r.status_code, r.json())

# GET /courses/{id}/students/
course_id = course['id']
r2 = client.get(f'/api/courses/{course_id}/students/')
print('GET /courses/id/students/ ->', r2.status_code, [s['first_name'] for s in r2.json()])

# PUT update
r3 = client.put(f'/api/courses/{course_id}/', json={'credits': 4})
print('PUT /courses/id/ ->', r3.status_code, 'credits:', r3.json()['credits'])

# DELETE 204
student_id = student['id']
r4 = client.delete(f'/api/students/{student_id}/')
print('DELETE /students/id/ ->', r4.status_code)

# Duplicate enrollment 409
s2 = client.post('/api/students/', json={'first_name': 'Bob', 'last_name': 'J', 'email': 'b@college.edu', 'department_id': dept['id'], 'enrollment_year': 2023}).json()
client.post('/api/enrollments/', json={'student_id': s2['id'], 'course_id': course_id})
r5 = client.post('/api/enrollments/', json={'student_id': s2['id'], 'course_id': course_id})
print('Duplicate enrollment ->', r5.status_code, r5.json()['detail'])
