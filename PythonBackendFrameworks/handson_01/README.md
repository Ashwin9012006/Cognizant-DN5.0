# Hands-On 1 - Web Framework Foundations & Django Setup

## Objective

The objective of this hands-on is to understand the fundamentals of web frameworks and set up a basic Django project. It covers the request-response lifecycle, middleware, web server interfaces, MVC vs MVT architecture, and creating the first Django application.

---

## Topics Covered

- Request-Response Cycle
- Django Project Structure
- Middleware
- WSGI and ASGI
- MVC vs MVT Architecture
- URL Routing
- Django Views

---

## Project Structure

```
handson_01/
│
├── coursemanager/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── courses/
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── notes.py
└── README.md
```

---

## Implementation

Completed the following tasks:

- Created the Django project **coursemanager**
- Created the **courses** application
- Registered the application in `INSTALLED_APPS`
- Added descriptive comments to project configuration files
- Implemented a simple `hello_view`
- Configured URL routing
- Tested the API endpoint successfully

---

## API Endpoint

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/hello/ | Returns a welcome message |

---

## Verification

The endpoint returned:

- HTTP 200 OK
- "Course Management API is running"

---

## Technologies Used

- Python
- Django

---

## Outcome

Successfully created a Django project, configured application routing, understood the web request lifecycle, and verified the first API endpoint.
