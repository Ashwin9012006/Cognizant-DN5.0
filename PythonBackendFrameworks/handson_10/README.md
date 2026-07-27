# Microservices Architecture - Hands-On 10
# README: Bounded Context Matrix & Architecture Overview

## Architecture

This hands-on implements a Microservices decomposition of the Course Management system.

### Services

| Service          | Port | Database            | Responsibilities                            |
|------------------|------|---------------------|---------------------------------------------|
| API Gateway      | 5000 | None                | Route/proxy requests, single entry point    |
| Course Service   | 5001 | course_service.db   | Departments, Courses                        |
| Student Service  | 5002 | student_service.db  | Students, Enrollments                       |

### Bounded Context Matrix

| Domain Entity   | Owns Data?  | Service         |
|-----------------|-------------|-----------------|
| Department      | Yes         | Course Service  |
| Course          | Yes         | Course Service  |
| Student         | Yes         | Student Service |
| Enrollment      | Yes         | Student Service |
| Course (ref)    | No (ref ID) | Student Service |

The Student Service stores `course_id` as a plain integer foreign reference, NOT a DB foreign key.
It validates the course exists via a synchronous HTTP call to Course Service at enrollment time.

### Inter-Service Communication

**Synchronous HTTP (Used in this hands-on):**
- Student Service calls `GET /api/courses/{id}/` on Course Service before enrolling.
- Pros: Simple, easy to implement, immediate validation feedback.
- Cons: Tight coupling, single point of failure if Course Service is down.
- Failure handling: Returns 503 Service Unavailable if Course Service is unreachable.

**Asynchronous Messaging (Alternative — e.g., RabbitMQ, Kafka):**
- Student Service publishes `enrollment_requested` event to message queue.
- Course Service consumes event, validates, and publishes `enrollment_confirmed` or `enrollment_rejected`.
- Student Service consumes the response and updates the enrollment record.
- Pros: Decoupled services, higher resilience, better scalability.
- Cons: More complex, eventual consistency, harder to debug.

### Running the Services

```bash
# Terminal 1 - Start Course Service
cd handson_10/course_service
python app.py

# Terminal 2 - Start Student Service
cd handson_10/student_service
python app.py

# Terminal 3 - Start API Gateway
cd handson_10/gateway
python app.py

# Test via Gateway
curl http://localhost:5000/health/
curl -X POST http://localhost:5000/api/v1/departments/ -H "Content-Type: application/json" -d '{"name":"CS","head_of_dept":"Dr. T"}'
curl -X POST http://localhost:5000/api/v1/courses/ -H "Content-Type: application/json" -d '{"name":"Algorithms","code":"CS201","credits":3,"department_id":1}'
curl -X POST http://localhost:5000/api/v1/students/ -H "Content-Type: application/json" -d '{"first_name":"Alice","last_name":"S","email":"a@c.edu","enrollment_year":2023}'
curl -X POST http://localhost:5000/api/v1/enrollments/ -H "Content-Type: application/json" -d '{"student_id":1,"course_id":1}'
```
