# Hands-On 8 - RESTful API Design Best Practices

## Objective

This hands-on focuses on designing REST APIs by following industry-standard conventions for versioning, resource naming, pagination, filtering, and error handling.

---

## Features

- API Versioning
- Resource Naming
- Pagination
- Search
- PATCH Endpoint
- Location Header
- Standard Error Format

---

## REST Standards

Implemented:

- Versioned APIs

```
/api/v1/
```

- Plural resource names

```
/courses
/students
```

---

## Pagination

Response format:

```json
{
    "count":20,
    "next":null,
    "previous":null,
    "results":[]
}
```

---

## Search

Supports case-insensitive search using

```
?search=
```

---

## Error Format

```json
{
    "error":{
        "code":"ERROR_CODE",
        "message":"Description",
        "field":null
    }
}
```

---

## Technologies Used

- FastAPI
- REST API Principles

---

## Outcome

Successfully implemented RESTful API standards including versioning, pagination, filtering, PATCH support, and consistent error responses.
