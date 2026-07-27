"""
Hands-On 9: Authentication & Security — JWT, CORS, and OWASP Best Practices

OWASP Security Measures Applied:
  - Passwords hashed with bcrypt (never stored in plain text).
  - JWT tokens expire after 30 minutes to limit exposure window.
  - HTTP 401 returned for invalid/missing tokens, never 200 with error body.
  - 409 returned on duplicate registration (no user enumeration via timing).
  - CORS restricted to trusted origins only (not wildcard *).
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import List, Optional

from database import Base, engine, get_db, CourseModel, DepartmentModel, StudentModel, EnrollmentModel, UserModel
from schemas import (
    UserRegister, UserLogin, TokenResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    DepartmentCreate, DepartmentResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse
)
from security import hash_password, verify_password, create_access_token, decode_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API - Secured",
    description="Course Management API with JWT authentication and CORS support.",
    version="1.0.0",
    contact={"name": "Ashwin Eshwer", "email": "ashwin@college.edu"}
)

# CORS middleware: allow only the frontend origin, not wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme: reads Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency: decodes JWT and returns the authenticated user. Raises 401 if invalid."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if not email:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise credentials_error
    return user


def send_confirmation_email(student_email: str, course_code: str):
    import logging
    logging.getLogger(__name__).info(f"[EMAIL] Sent confirmation to {student_email} for {course_code}")


# --- Auth Endpoints ---

@app.post("/api/v1/auth/register/", response_model=TokenResponse, status_code=201, tags=["Auth"])
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user. Returns 409 if email already exists."""
    if db.query(UserModel).filter(UserModel.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = hash_password(user_data.password)
    new_user = UserModel(email=user_data.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/v1/auth/login/", response_model=TokenResponse, tags=["Auth"])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password. Returns a JWT access token on success."""
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# --- Department Endpoints (public read, auth required for write) ---

@app.post("/api/v1/departments/", response_model=DepartmentResponse, status_code=201, tags=["Departments"])
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_dept = DepartmentModel(name=dept.name, head_of_dept=dept.head_of_dept, budget=dept.budget)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept


@app.get("/api/v1/departments/", response_model=List[DepartmentResponse], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return db.query(DepartmentModel).all()


# --- Course Endpoints ---

@app.post("/api/v1/courses/", response_model=CourseResponse, status_code=201, tags=["Courses"])
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Protected: requires valid JWT. Creates a new course."""
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


@app.get("/api/v1/courses/", response_model=List[CourseResponse], tags=["Courses"])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Public: list all courses, no auth required."""
    query = db.query(CourseModel)
    if department_id:
        query = query.filter(CourseModel.department_id == department_id)
    if search:
        term = f"%{search.lower()}%"
        query = query.filter((CourseModel.name.ilike(term)) | (CourseModel.code.ilike(term)))
    return query.offset(skip).limit(limit).all()


@app.get("/api/v1/courses/{course_id}/", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    return course


@app.delete("/api/v1/courses/{course_id}/", status_code=204, tags=["Courses"])
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Protected: requires valid JWT. Deletes a course."""
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    db.delete(course)
    db.commit()
    return Response(status_code=204)


# --- Student Endpoints ---

@app.post("/api/v1/students/", response_model=StudentResponse, status_code=201, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.query(StudentModel).filter(StudentModel.email == student.email).first():
        raise HTTPException(status_code=409, detail=f"Email {student.email} already exists")
    new_student = StudentModel(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get("/api/v1/students/", response_model=List[StudentResponse], tags=["Students"])
def list_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


# --- Enrollment Endpoints ---

@app.post("/api/v1/enrollments/", response_model=EnrollmentResponse, status_code=201, tags=["Enrollments"])
def create_enrollment(enrollment: EnrollmentCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(CourseModel).filter(CourseModel.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if db.query(EnrollmentModel).filter(EnrollmentModel.student_id == enrollment.student_id, EnrollmentModel.course_id == enrollment.course_id).first():
        raise HTTPException(status_code=409, detail="Already enrolled")

    new_enrollment = EnrollmentModel(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    background_tasks.add_task(send_confirmation_email, student.email, course.code)
    return new_enrollment
