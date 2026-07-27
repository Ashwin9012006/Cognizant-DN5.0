from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks, Response
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

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="RESTful API for managing courses, students, departments, and enrollments.",
    version="1.0.0",
    contact={"name": "Ashwin Eshwer", "email": "ashwin@college.edu"},
    license_info={"name": "MIT"}
)


# --- Background Task ---

def send_confirmation_email(student_email: str, course_code: str):
    """Background task: simulates sending an enrollment confirmation email."""
    logger.info(f"[EMAIL] Sending enrollment confirmation to {student_email} for course {course_code}")


# --- Department Endpoints ---

@app.post(
    "/api/departments/",
    response_model=DepartmentResponse,
    status_code=201,
    tags=["Departments"],
    summary="Create a new department",
    response_description="The newly created department"
)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new academic department with a name, head, and budget."""
    new_dept = DepartmentModel(name=dept.name, head_of_dept=dept.head_of_dept, budget=dept.budget)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept


@app.get(
    "/api/departments/",
    response_model=List[DepartmentResponse],
    tags=["Departments"],
    summary="List all departments"
)
def list_departments(db: Session = Depends(get_db)):
    return db.query(DepartmentModel).all()


# --- Course Endpoints ---

@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=201,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The newly created course"
)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course. Validates that the department exists and the code is unique."""
    dept = db.query(DepartmentModel).filter(DepartmentModel.id == course.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail=f"Department {course.department_id} not found")

    if db.query(CourseModel).filter(CourseModel.code == course.code).first():
        raise HTTPException(status_code=409, detail=f"Course code {course.code} already exists")

    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get(
    "/api/courses/",
    response_model=List[CourseResponse],
    tags=["Courses"],
    summary="List all courses with pagination"
)
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get a paginated list of courses. Optionally filter by department_id."""
    query = db.query(CourseModel)
    if department_id:
        query = query.filter(CourseModel.department_id == department_id)
    return query.offset(skip).limit(limit).all()


@app.get(
    "/api/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Get a course by ID"
)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    return course


@app.put(
    "/api/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Update a course"
)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """Update an existing course's fields."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

    update_fields = course_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


@app.delete(
    "/api/courses/{course_id}/",
    status_code=204,
    tags=["Courses"],
    summary="Delete a course"
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course by ID. Returns 204 No Content on success."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    db.delete(course)
    db.commit()
    return Response(status_code=204)


@app.get(
    "/api/courses/{course_id}/students/",
    response_model=List[StudentResponse],
    tags=["Courses"],
    summary="Get all students enrolled in a course"
)
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    """Returns all students enrolled in a specific course using a JOIN query."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

    students = (
        db.query(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .filter(EnrollmentModel.course_id == course_id)
        .all()
    )
    return students


# --- Student Endpoints ---

@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=201,
    tags=["Students"],
    summary="Create a new student"
)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.query(StudentModel).filter(StudentModel.email == student.email).first():
        raise HTTPException(status_code=409, detail=f"Email {student.email} already exists")
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get(
    "/api/students/",
    response_model=List[StudentResponse],
    tags=["Students"],
    summary="List all students"
)
def list_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


@app.delete(
    "/api/students/{student_id}/",
    status_code=204,
    tags=["Students"],
    summary="Delete a student"
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    db.delete(student)
    db.commit()
    return Response(status_code=204)


# --- Enrollment Endpoints ---

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=201,
    tags=["Enrollments"],
    summary="Enroll a student in a course"
)
def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Enrolls a student in a course. Validates student and course exist, checks for duplicate enrollment.
    Sends a confirmation email in the background after successful enrollment.
    """
    student = db.query(StudentModel).filter(StudentModel.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {enrollment.student_id} not found")

    course = db.query(CourseModel).filter(CourseModel.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {enrollment.course_id} not found")

    existing = db.query(EnrollmentModel).filter(
        EnrollmentModel.student_id == enrollment.student_id,
        EnrollmentModel.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    # Trigger background task to send enrollment confirmation email
    background_tasks.add_task(send_confirmation_email, student.email, course.code)

    return new_enrollment


@app.get(
    "/api/enrollments/",
    response_model=List[EnrollmentResponse],
    tags=["Enrollments"],
    summary="List all enrollments"
)
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(EnrollmentModel).all()
