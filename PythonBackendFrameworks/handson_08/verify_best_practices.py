from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=== TESTING HANDS-ON 8: REST Best Practices ===")

# Create department
dept = client.post('/api/v1/departments/', json={'name': 'CS', 'head_of_dept': 'Dr. T', 'budget': 90000.0}).json()
print('POST /api/v1/departments/ ->', dept.get('id') or dept)

# Create courses
c1 = client.post('/api/v1/courses/', json={'name': 'Algorithms', 'code': 'CS201', 'credits': 3, 'department_id': dept['id']})
print('POST /api/v1/courses/ ->', c1.status_code, c1.headers.get('location'), '(Location header)')
course_id = c1.json()['id']

c2 = client.post('/api/v1/courses/', json={'name': 'Web Development', 'code': 'CS301', 'credits': 3, 'department_id': dept['id']})

# Paginated listing
r = client.get('/api/v1/courses/?skip=0&limit=10')
data = r.json()
print('GET /api/v1/courses/ paginated ->', r.status_code, 'count:', data['count'], 'results:', len(data['results']))
print('  next:', data['next'], 'previous:', data['previous'])

# Search filter
r2 = client.get('/api/v1/courses/?search=algo')
data2 = r2.json()
print('GET /api/v1/courses/?search=algo ->', r2.status_code, 'count:', data2['count'])

# PATCH partial update
r3 = client.patch(f'/api/v1/courses/{course_id}/', json={'credits': 4})
print('PATCH /api/v1/courses/id/ ->', r3.status_code, 'credits:', r3.json()['credits'])

# Error envelope
r4 = client.get('/api/v1/courses/9999/')
print('GET nonexistent ->', r4.status_code, r4.json())

# Standardized error on duplicate code
r5 = client.post('/api/v1/courses/', json={'name': 'Dup', 'code': 'CS201', 'credits': 2, 'department_id': dept['id']})
print('POST duplicate code error ->', r5.status_code, r5.json())
