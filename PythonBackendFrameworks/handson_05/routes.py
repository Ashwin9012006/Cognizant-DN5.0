from flask import Blueprint, request, jsonify
from courses.models import db, Department, Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api')


@courses_bp.route('/courses/', methods=['GET'])
def get_courses():
    """GET /api/courses/ -> list all courses with optional department_id filter."""
    dept_id = request.args.get('department_id', type=int)
    if dept_id:
        courses = Course.query.filter_by(department_id=dept_id).all()
    else:
        courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses]), 200


@courses_bp.route('/courses/', methods=['POST'])
def create_course():
    """POST /api/courses/ -> create a new course."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required = ['name', 'code', 'credits', 'department_id']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    # Check dept exists
    dept = Department.query.get(data['department_id'])
    if not dept:
        return jsonify({'error': f'Department {data["department_id"]} not found'}), 404

    # Check code uniqueness
    if Course.query.filter_by(code=data['code']).first():
        return jsonify({'error': f'Course code {data["code"]} already exists'}), 409

    course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data['department_id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@courses_bp.route('/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """GET /api/courses/<course_id>/ -> get course by ID."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404
    return jsonify(course.to_dict()), 200


@courses_bp.route('/courses/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    """PUT /api/courses/<course_id>/ -> update course fields."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        course.name = data['name']
    if 'code' in data:
        course.code = data['code']
    if 'credits' in data:
        course.credits = data['credits']
    db.session.commit()
    return jsonify(course.to_dict()), 200


@courses_bp.route('/courses/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    """DELETE /api/courses/<course_id>/ -> delete course."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': f'Course {course_id} deleted successfully'}), 200


@courses_bp.route('/courses/<int:course_id>/students/', methods=['GET'])
def get_course_students(course_id):
    """GET /api/courses/<course_id>/students/ -> students enrolled in a course using JOIN query."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404

    # Join query through Enrollment to find all students for this course
    students = (
        Student.query
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course_id)
        .all()
    )
    return jsonify([s.to_dict() for s in students]), 200


@courses_bp.route('/departments/', methods=['GET'])
def get_departments():
    """GET /api/departments/ -> list all departments."""
    departments = Department.query.all()
    return jsonify([d.to_dict() for d in departments]), 200


@courses_bp.route('/departments/', methods=['POST'])
def create_department():
    """POST /api/departments/ -> create new department."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required = ['name', 'head_of_dept', 'budget']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    dept = Department(name=data['name'], head_of_dept=data['head_of_dept'], budget=data['budget'])
    db.session.add(dept)
    db.session.commit()
    return jsonify(dept.to_dict()), 201


@courses_bp.route('/students/', methods=['GET'])
def get_students():
    """GET /api/students/ -> list all students."""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


@courses_bp.route('/students/', methods=['POST'])
def create_student():
    """POST /api/students/ -> create a new student."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required = ['first_name', 'last_name', 'email', 'department_id', 'enrollment_year']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': f'Student with email {data["email"]} already exists'}), 409

    student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        department_id=data['department_id'],
        enrollment_year=data['enrollment_year']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@courses_bp.route('/enrollments/', methods=['GET'])
def get_enrollments():
    """GET /api/enrollments/ -> list all enrollments."""
    enrollments = Enrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments]), 200


@courses_bp.route('/enrollments/', methods=['POST'])
def create_enrollment():
    """POST /api/enrollments/ -> enroll a student in a course."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required = ['student_id', 'course_id']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    # Check for duplicate enrollment
    existing = Enrollment.query.filter_by(
        student_id=data['student_id'],
        course_id=data['course_id']
    ).first()
    if existing:
        return jsonify({'error': 'Student is already enrolled in this course'}), 409

    enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id'],
        grade=data.get('grade')
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201
