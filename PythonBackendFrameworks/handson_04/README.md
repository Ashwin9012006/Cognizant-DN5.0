# Hands-On 4 - Flask Application Structure & Blueprints

## Objective

The purpose of this hands-on is to understand how a Flask application can be organized using the Application Factory pattern and Blueprints. The project also demonstrates configuration management, JSON responses, request validation, and global error handling.

---

## Features

- Application Factory (`create_app()`)
- Configuration class (`Config`)
- Blueprint-based routing
- Standard JSON response format
- Input validation
- Global error handlers
- REST API structure

---

## Project Structure

```
handson_04/
│
├── app.py
├── config.py
├── requirements.txt
├── courses/
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/courses | Retrieve all courses |
| POST | /api/courses | Create a new course |

---

## Validation

The POST endpoint validates:

- Course Name
- Course Code
- Credits

If any field is missing, the API returns HTTP 400.

Example:

```json
{
    "status":"error",
    "message":"Required fields are missing"
}
```

---

## Error Handling

Implemented global handlers for

- HTTP 404
- HTTP 500

All errors return JSON instead of the default HTML error page.

---

## Technologies Used

- Python
- Flask
- Blueprint
- JSON API

---

## Outcome

Successfully created a modular Flask application following best practices for project organization and REST API development.
