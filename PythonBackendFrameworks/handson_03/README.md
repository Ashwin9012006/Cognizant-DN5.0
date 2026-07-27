# Hands-On 3 - Django REST Framework (DRF)

## Objective

The objective of this hands-on is to build RESTful APIs using Django REST Framework by implementing serializers, API views, viewsets, routers, and custom actions.

---

## Features

- Model Serializers
- APIView
- ModelViewSet
- DefaultRouter
- CRUD Operations
- Custom Actions
- REST API Development

---

## Components

Implemented serializers for:

- Department
- Course
- Student
- Enrollment

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/courses/ | Retrieve all courses |
| POST | /api/courses/ | Create a course |
| GET | /api/courses/{id}/ | Retrieve course details |
| PUT | /api/courses/{id}/ | Update course |
| DELETE | /api/courses/{id}/ | Delete course |

---

## Custom Endpoint

Implemented a custom action:

```
GET /api/courses/{id}/students/
```

Returns all students enrolled in the selected course.

---

## Verification

Verified using the testing script:

- GET
- POST
- PUT
- DELETE
- Custom action endpoint

All endpoints returned the expected responses.

---

## Technologies Used

- Django
- Django REST Framework
- SQLite

---

## Outcome

Successfully developed RESTful APIs using Django REST Framework with serializers, API views, viewsets, routers, and custom endpoints following REST principles.
