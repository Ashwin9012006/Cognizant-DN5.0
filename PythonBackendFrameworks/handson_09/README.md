# Hands-On 9 - Authentication & API Security

## Objective

The objective of this hands-on is to secure REST APIs using JWT authentication, password hashing, protected routes, and CORS configuration.

---

## Features

- User Registration
- User Login
- JWT Authentication
- Password Hashing
- Protected APIs
- CORS Configuration

---

## Authentication Flow

1. Register User
2. Password Hashing using bcrypt
3. Login
4. Generate JWT Token
5. Access Protected Endpoints

---

## Security

Implemented:

- bcrypt password hashing
- JWT authentication
- Protected routes
- Duplicate user validation
- Unauthorized request handling

---

## CORS

Allowed origin:

```
http://localhost:3000
```

---

## Endpoints

| Method | Endpoint |
|---------|----------|
|POST|/api/v1/auth/register|
|POST|/api/v1/auth/login|

---

## Technologies Used

- FastAPI
- bcrypt
- python-jose
- JWT

---

## Outcome

Successfully implemented secure authentication using JWT tokens and protected API endpoints following modern web security practices.
