from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=== TESTING HANDS-ON 9: JWT Authentication & Security ===")

# Test register
r = client.post('/api/v1/auth/register/', json={'email': 'ashwin@college.edu', 'password': 'Secret@123'})
print('POST /auth/register/ ->', r.status_code, 'token_type:', r.json().get('token_type'))
token = r.json()['access_token']

# Test duplicate register (409)
r2 = client.post('/api/v1/auth/register/', json={'email': 'ashwin@college.edu', 'password': 'Secret@123'})
print('POST /auth/register/ duplicate ->', r2.status_code, r2.json()['detail'])

# Test login
r3 = client.post('/api/v1/auth/login/', json={'email': 'ashwin@college.edu', 'password': 'Secret@123'})
print('POST /auth/login/ ->', r3.status_code, 'token received:', bool(r3.json().get('access_token')))

# Test bad login
r4 = client.post('/api/v1/auth/login/', json={'email': 'ashwin@college.edu', 'password': 'wrongpass'})
print('POST /auth/login/ bad pass ->', r4.status_code, r4.json()['detail'])

# Test protected endpoint without token (401)
r5 = client.post('/api/v1/courses/', json={'name': 'CS101', 'code': 'CS101', 'credits': 3, 'department_id': 1})
print('POST /courses/ without auth ->', r5.status_code)

# Test protected endpoint with token (create dept first)
headers = {'Authorization': f'Bearer {token}'}
dept_r = client.post('/api/v1/departments/', json={'name': 'CS', 'head_of_dept': 'Dr. T', 'budget': 90000.0}, headers=headers)
dept_id = dept_r.json()['id']
print('POST /departments/ with auth ->', dept_r.status_code)

course_r = client.post('/api/v1/courses/', json={'name': 'Algorithms', 'code': 'CS201', 'credits': 3, 'department_id': dept_id}, headers=headers)
print('POST /courses/ with auth ->', course_r.status_code, course_r.json().get('code'))

# Public GET (no auth)
pub_r = client.get('/api/v1/courses/')
print('GET /courses/ public ->', pub_r.status_code, len(pub_r.json()), 'courses')

# DELETE with auth (204)
course_id = course_r.json()['id']
del_r = client.delete(f'/api/v1/courses/{course_id}/', headers=headers)
print('DELETE /courses/id/ with auth ->', del_r.status_code)
