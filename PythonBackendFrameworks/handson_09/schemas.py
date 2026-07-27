from pydantic import BaseModel, field_validator
from typing import Optional

# --- Auth Schemas ---

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Department Schemas ---

class DepartmentCreate(BaseModel):
    name: str
    head_of_dept: str
    budget: float

class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float

    model_config = {"from_attributes": True}


# --- Course Schemas ---

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int = 3
    department_id: int

    @field_validator('credits')
    @classmethod
    def credits_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('credits must be a positive integer')
        return v

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    model_config = {"from_attributes": True}


# --- Student Schemas ---

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int
    enrollment_year: int

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int
    enrollment_year: int

    model_config = {"from_attributes": True}


# --- Enrollment Schemas ---

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: Optional[str]

    model_config = {"from_attributes": True}
