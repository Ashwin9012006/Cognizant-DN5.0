# Hands-On 5 - Flask with SQLAlchemy ORM

## Objective

This hands-on demonstrates database integration in Flask using SQLAlchemy ORM. It replaces in-memory data with persistent database storage and performs CRUD operations using ORM queries.

---

## Features

- SQLAlchemy ORM
- Flask-Migrate
- Database models
- CRUD operations
- Database seeding
- JOIN queries
- Model serialization

---

## Project Structure

```
handson_05/
│
├── app.py
├── courses/
│   ├── models.py
│   ├── routes.py
│   └── database.py
├── migrations/
├── verify_flask_orm.py
└── README.md
```

---

## Database Models

- Department
- Course
- Student
- Enrollment

Each model includes a `to_dict()` method for JSON serialization.

---

## Implemented Operations

- Retrieve all courses
- Retrieve course by ID
- Create course
- Update course
- Delete course
- Student enrollment
- JOIN query to retrieve enrolled students

---

## Verification

The verification script checks:

- Database creation
- Sample data insertion
- CRUD functionality
- JOIN queries

---

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite

---

## Outcome

Successfully implemented database persistence using SQLAlchemy and integrated ORM operations into the Flask REST API.
