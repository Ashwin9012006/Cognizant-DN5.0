from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Using synchronous SQLite for simplicity in this hands-on
DATABASE_URL = "sqlite:///./coursemanager.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DepartmentModel(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100), nullable=False)
    budget = Column(Numeric(12, 2), nullable=False)


class CourseModel(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    credits = Column(Integer, default=3)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)


class StudentModel(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    enrollment_year = Column(Integer, nullable=False)


class EnrollmentModel(Base):
    __tablename__ = "enrollment"
    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='uq_student_course'),)

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    grade = Column(String(5), nullable=True)


def get_db():
    """FastAPI dependency injection: yields a DB session, then closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
