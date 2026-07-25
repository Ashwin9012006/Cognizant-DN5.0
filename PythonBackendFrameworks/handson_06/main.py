from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import Base, engine, get_db, CourseModel, DepartmentModel, StudentModel
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    DepartmentCreate, DepartmentResponse,
    StudentCreate, StudentResponse
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="A FastAPI-based course management REST API",
    version="1.0.0"
)


@app.get("/", summary="Health Check")
def health_check():
    """Root endpoint to confirm the API is running."""
    return {"message": "Course Management API is running"}


# --- Department Endpoints ---

@app.post("/api/departments/", response_model=DepartmentResponse, status_code=201, tags=["Departments"])
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department."""
    new_dept = DepartmentModel(name=dept.name, head_of_dept=dept.head_of_dept, budget=dept.budget)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept


@app.get("/api/departments/", response_model=List[DepartmentResponse], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    """Get all departments."""
    return db.query(DepartmentModel).all()


# --- Course Endpoints ---

@app.post("/api/courses/", response_model=CourseResponse, status_code=201, tags=["Courses"])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course. Returns 404 if department does not exist, 409 if code already taken."""
    # Validate department exists
    dept = db.query(DepartmentModel).filter(DepartmentModel.id == course.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail=f"Department {course.department_id} not found")

    # Validate unique code
    existing = db.query(CourseModel).filter(CourseModel.code == course.code).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Course code {course.code} already exists")

    new_course = CourseModel(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
def list_courses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    db: Session = Depends(get_db)
):
    """List all courses with pagination and optional filtering by department."""
    query = db.query(CourseModel)
    if department_id:
        query = query.filter(CourseModel.department_id == department_id)
    return query.offset(skip).limit(limit).all()


@app.get("/api/courses/{course_id}/", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a single course by ID."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    return course


# --- Student Endpoints ---

@app.post("/api/students/", response_model=StudentResponse, status_code=201, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student. Returns 409 if email already exists."""
    existing = db.query(StudentModel).filter(StudentModel.email == student.email).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Student with email {student.email} already exists")

    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get("/api/students/", response_model=List[StudentResponse], tags=["Students"])
def list_students(db: Session = Depends(get_db)):
    """List all students."""
    return db.query(StudentModel).all()
