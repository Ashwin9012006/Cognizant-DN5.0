import sys
sys.path.insert(0, '.')
from app import create_app
from courses.models import db, Department, Course, Student, Enrollment
from datetime import date

app = create_app()

with app.app_context():
    db.create_all()

    # Only seed if empty
    if Department.query.count() == 0:
        cs = Department(name='Computer Science', head_of_dept='Dr. Turing', budget=100000)
        db.session.add(cs)
        db.session.flush()

        c1 = Course(name='Intro to CS', code='CS101', credits=4, department_id=cs.id)
        c2 = Course(name='Data Structures', code='CS102', credits=4, department_id=cs.id)
        db.session.add_all([c1, c2])
        db.session.flush()

        s1 = Student(first_name='Alice', last_name='Smith', email='alice@college.edu', department_id=cs.id, enrollment_year=2023)
        s2 = Student(first_name='Bob', last_name='Jones', email='bob@college.edu', department_id=cs.id, enrollment_year=2023)
        db.session.add_all([s1, s2])
        db.session.flush()

        e1 = Enrollment(student_id=s1.id, course_id=c1.id, grade='A', enrollment_date=date.today())
        e2 = Enrollment(student_id=s2.id, course_id=c1.id, grade='B', enrollment_date=date.today())
        db.session.add_all([e1, e2])
        db.session.commit()
        print('DB seeded OK')
    else:
        print('DB already has data')

with app.test_client() as c:
    r = c.get('/api/courses/')
    data = r.get_json()
    print('GET /api/courses/ ->', r.status_code, len(data), 'courses')

    r2 = c.get('/api/courses/1/students/')
    students = r2.get_json()
    print('GET /api/courses/1/students/ ->', r2.status_code, [s['first_name'] for s in students])

    r3 = c.get('/api/departments/')
    print('GET /api/departments/ ->', r3.status_code, len(r3.get_json()), 'departments')
