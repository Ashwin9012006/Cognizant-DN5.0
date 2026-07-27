# Hands-On 2 - Django Models, ORM & Admin Interface

## Objective

This hands-on focuses on designing database models using Django ORM, configuring the Django Admin interface, and performing database operations using ORM queries.

---

## Features

- Django Models
- Relationships
- Django ORM
- Django Admin
- Aggregation
- Query Optimization
- Database Constraints

---

## Database Models

The following models were created:

- Department
- Course
- Student
- Enrollment

Relationships were implemented using ForeignKey associations.

---

## Admin Configuration

Registered all models in the Django Admin panel.

Customized the Course model with:

- list_display
- search_fields
- list_filter

---

## ORM Operations

Performed the following operations:

- Record creation
- Filtering
- Aggregation
- JOIN optimization using `select_related()`
- Atomic updates using `F()` expressions
- Constraint validation

---

## Verification

The ORM verification script tested:

- Department-based filtering
- Course count aggregation
- Optimized JOIN queries
- Budget updates
- Duplicate enrollment prevention

---

## Technologies Used

- Django
- Django ORM
- SQLite

---

## Outcome

Successfully implemented relational database models, configured the Django Admin interface, and performed efficient ORM operations with built-in constraint validation.
