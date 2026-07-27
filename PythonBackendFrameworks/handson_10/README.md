# Hands-On 10 - Microservices Architecture

## Objective

The objective of this hands-on is to understand how a monolithic application can be divided into multiple independent services using a microservices architecture.

---

## Services

### Course Service

Responsible for:

- Departments
- Courses

Runs on:

```
Port 5001
```

---

### Student Service

Responsible for:

- Students
- Enrollments

Runs on:

```
Port 5002
```

---

### API Gateway

Acts as the entry point for client requests and forwards them to the appropriate backend service.

Runs on:

```
Port 5000
```

---

## Features

- Service Separation
- API Gateway
- Inter-Service Communication
- HTTP Validation
- Fault Tolerance

---

## Service Communication

Student Service validates course availability by making an HTTP request to Course Service before creating an enrollment.

If Course Service is unavailable, the API returns:

```
HTTP 503 Service Unavailable
```

---

## Project Components

- Course Service
- Student Service
- API Gateway
- SQLite Databases
- README Documentation

---

## Technologies Used

- Flask
- SQLite
- Requests Library

---

## Outcome

Successfully implemented a simple microservices architecture with independent services, API Gateway routing, inter-service communication, and basic fault tolerance mechanisms.
