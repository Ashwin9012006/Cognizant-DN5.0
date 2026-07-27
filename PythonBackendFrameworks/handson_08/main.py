"""
Hands-On 8: RESTful API Design Best Practices

This module implements a versioned REST API following industry best practices:

URL VERSIONING STRATEGY:
- We use URL path versioning: /api/v1/courses/
- Advantages: Easy to see in browser/logs, simple client implementation, cacheable
- Alternative (Header versioning): Accept: application/vnd.api+json;version=1
  Advantages: Cleaner URLs, follows HTTP spec
  Disadvantage: Harder to test in browser, more complex client code

REST BEST PRACTICES APPLIED:
1. Plural resource nouns: /api/v1/courses/, /api/v1/students/
2. HTTP verbs for actions: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove)
3. Proper status codes: 200, 201, 204, 400, 404, 409, 422
4. Location header on POST: Location: /api/v1/courses/{id}/
5. Standardized error envelope: {"error": {"code": "...", "message": "..."}}
6. Pagination with envelope: {"count": N, "next": url, "previous": url, "results": [...]}
7. Filtering with query params: ?search=algo, ?department_id=1
"""

from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import Base, engine, get_db, CourseModel, DepartmentModel, StudentModel, EnrollmentModel
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    DepartmentCreate, DepartmentResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API v1",
    description="RESTful API following best practices — versioned, paginated, and standardized error responses.",
    version="1.0.0",
    contact={"name": "Ashwin Eshwer", "email": "ashwin@college.edu"}
)


def error_response(code: str, message: str, field: str = None, status_code: int = 400):
    """Returns a standardized error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "field": field}}
    )


def paginate(items: list, total_count: int, skip: int, limit: int, request: Request) -> dict:
    """Returns a paginated envelope with count, next, previous, and results."""
    base_url = str(request.base_url).rstrip('/')
    path = request.url.path

    next_url = f"{base_url}{path}?skip={skip + limit}&limit={limit}" if (skip + limit) < total_count else None
    prev_url = f"{base_url}{path}?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None

    return {
        "count": total_count,
        "next": next_url,
        "previous": prev_url,
        "results": items
    }


def send_confirmation_email(student_email: str, course_code: str):
    logger.info(f"[EMAIL] Confirmation sent to {student_email} for {course_code}")


# --- Department Endpoints (v1) ---

@app.post("/api/v1/departments/", response_model=DepartmentResponse, status_code=201, tags=["Departments"])
def create_department(dept: DepartmentCreate, request: Request, db: Session = Depends(get_db)):
    new_dept = DepartmentModel(name=dept.name, head_of_dept=dept.head_of_dept, budget=dept.budget)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    headers = {"Location": f"/api/v1/departments/{new_dept.id}/"}
    return JSONResponse(
        content={"id": new_dept.id, "name": new_dept.name, "head_of_dept": new_dept.head_of_dept, "budget": float(new_dept.budget)},
        status_code=201,
        headers=headers
    )


@app.get("/api/v1/departments/", tags=["Departments"])
def list_departments(request: Request, db: Session = Depends(get_db)):
    depts = db.query(DepartmentModel).all()
    results = [{"id": d.id, "name": d.name, "head_of_dept": d.head_of_dept, "budget": float(d.budget)} for d in depts]
    return paginate(results, len(results), 0, len(results) or 10, request)


# --- Course Endpoints (v1) ---

@app.post("/api/v1/courses/", response_model=CourseResponse, status_code=201, tags=["Courses"])
def create_course(course: CourseCreate, request: Request, db: Session = Depends(get_db)):
    """POST /api/v1/courses/ - Creates a course, returns Location header."""
    dept = db.query(DepartmentModel).filter(DepartmentModel.id == course.department_id).first()
    if not dept:
        return error_response("DEPT_NOT_FOUND", f"Department {course.department_id} not found", status_code=404)

    if db.query(CourseModel).filter(CourseModel.code == course.code).first():
        return error_response("CODE_EXISTS", f"Course code {course.code} already exists", status_code=409)

    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    # Best practice: Include Location header pointing to the created resource
    headers = {"Location": f"/api/v1/courses/{new_course.id}/"}
    return JSONResponse(
        content={"id": new_course.id, "name": new_course.name, "code": new_course.code, "credits": new_course.credits, "department_id": new_course.department_id},
        status_code=201,
        headers=headers
    )


@app.get("/api/v1/courses/", tags=["Courses"])
def list_courses(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items per page"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    search: Optional[str] = Query(None, description="Search in course name or code (case-insensitive)"),
    db: Session = Depends(get_db)
):
    """GET /api/v1/courses/ - Paginated and filterable course listing."""
    query = db.query(CourseModel)

    if department_id:
        query = query.filter(CourseModel.department_id == department_id)

    if search:
        # Case-insensitive search on name and code
        search_term = f"%{search.lower()}%"
        query = query.filter(
            (CourseModel.name.ilike(search_term)) | (CourseModel.code.ilike(search_term))
        )

    total = query.count()
    courses = query.offset(skip).limit(limit).all()
    results = [{"id": c.id, "name": c.name, "code": c.code, "credits": c.credits, "department_id": c.department_id} for c in courses]

    return paginate(results, total, skip, limit, request)


@app.get("/api/v1/courses/{course_id}/", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    return course


@app.put("/api/v1/courses/{course_id}/", response_model=CourseResponse, tags=["Courses"])
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """PUT - Full update (all fields)."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    for field, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.patch("/api/v1/courses/{course_id}/", response_model=CourseResponse, tags=["Courses"])
def partial_update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """PATCH - Partial update (only provided fields). Semantically same as PUT here since CourseUpdate is optional."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    for field, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/v1/courses/{course_id}/", status_code=204, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    db.delete(course)
    db.commit()
    return Response(status_code=204)


# --- Student Endpoints (v1) ---

@app.post("/api/v1/students/", response_model=StudentResponse, status_code=201, tags=["Students"])
def create_student(student: StudentCreate, request: Request, db: Session = Depends(get_db)):
    if db.query(StudentModel).filter(StudentModel.email == student.email).first():
        return error_response("EMAIL_EXISTS", f"Email {student.email} already registered", "email", 409)
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    headers = {"Location": f"/api/v1/students/{new_student.id}/"}
    return JSONResponse(
        content={"id": new_student.id, "first_name": new_student.first_name, "last_name": new_student.last_name, "email": new_student.email, "department_id": new_student.department_id, "enrollment_year": new_student.enrollment_year},
        status_code=201,
        headers=headers
    )


@app.get("/api/v1/students/", tags=["Students"])
def list_students(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(StudentModel).count()
    students = db.query(StudentModel).offset(skip).limit(limit).all()
    results = [{"id": s.id, "first_name": s.first_name, "last_name": s.last_name, "email": s.email, "department_id": s.department_id, "enrollment_year": s.enrollment_year} for s in students]
    return paginate(results, total, skip, limit, request)


# --- Enrollment Endpoints (v1) ---

@app.post("/api/v1/enrollments/", response_model=EnrollmentResponse, status_code=201, tags=["Enrollments"])
def create_enrollment(enrollment: EnrollmentCreate, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == enrollment.student_id).first()
    if not student:
        return error_response("STUDENT_NOT_FOUND", f"Student {enrollment.student_id} not found", status_code=404)

    course = db.query(CourseModel).filter(CourseModel.id == enrollment.course_id).first()
    if not course:
        return error_response("COURSE_NOT_FOUND", f"Course {enrollment.course_id} not found", status_code=404)

    if db.query(EnrollmentModel).filter(EnrollmentModel.student_id == enrollment.student_id, EnrollmentModel.course_id == enrollment.course_id).first():
        return error_response("ALREADY_ENROLLED", "Student is already enrolled in this course", status_code=409)

    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email, course.code)
    headers = {"Location": f"/api/v1/enrollments/{new_enrollment.id}/"}
    return JSONResponse(
        content={"id": new_enrollment.id, "student_id": new_enrollment.student_id, "course_id": new_enrollment.course_id, "grade": new_enrollment.grade},
        status_code=201,
        headers=headers
    )


@app.get("/api/v1/enrollments/", tags=["Enrollments"])
def list_enrollments(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(EnrollmentModel).count()
    enrollments = db.query(EnrollmentModel).offset(skip).limit(limit).all()
    results = [{"id": e.id, "student_id": e.student_id, "course_id": e.course_id, "grade": e.grade} for e in enrollments]
    return paginate(results, total, skip, limit, request)
