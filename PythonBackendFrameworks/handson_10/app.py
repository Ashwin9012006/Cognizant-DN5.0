# Student Service - Hands-On 10 Microservices
# Runs on port 5002, owns its own independent SQLite database for students & enrollments.
# Makes inter-service HTTP calls to Course Service (port 5001) to validate course existence.

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Base URL of the Course Service - in production this would come from service registry / env variable
COURSE_SERVICE_URL = 'http://localhost:5001'


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'enrollment_year': self.enrollment_year}


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)  # References Course Service, not local FK
    grade = db.Column(db.String(5), nullable=True)

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id, 'course_id': self.course_id, 'grade': self.grade}


with app.app_context():
    db.create_all()


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400

    required = ['first_name', 'last_name', 'email', 'enrollment_year']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing: {", ".join(missing)}'}), 400

    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        enrollment_year=data['enrollment_year']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/enrollments/', methods=['POST'])
def create_enrollment():
    """
    Enroll a student in a course. Makes a synchronous HTTP call to Course Service
    to verify the course exists before creating the enrollment record locally.
    
    Inter-service communication strategy:
    - Synchronous HTTP (used here): Simple, easy to implement. Best for request-response.
    - Asynchronous messaging (e.g. RabbitMQ/Kafka): Better for high-throughput, decoupled scenarios.
      The student service would publish an 'enrollment_requested' event; Course Service confirms async.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400

    student = Student.query.get(data.get('student_id'))
    if not student:
        return jsonify({'error': f'Student {data.get("student_id")} not found'}), 404

    # Inter-service call to Course Service to validate course existence
    try:
        course_resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{data["course_id"]}/', timeout=3)
        if course_resp.status_code == 404:
            return jsonify({'error': f'Course {data["course_id"]} not found in Course Service'}), 404
        if course_resp.status_code != 200:
            return jsonify({'error': 'Course Service returned an unexpected error'}), 502
    except requests.exceptions.ConnectionError:
        # Handle case where Course Service is down
        return jsonify({'error': 'Course Service is unavailable. Please try again later.'}), 503

    existing = Enrollment.query.filter_by(student_id=data['student_id'], course_id=data['course_id']).first()
    if existing:
        return jsonify({'error': 'Student already enrolled in this course'}), 409

    enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'], grade=data.get('grade'))
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201


@app.route('/api/enrollments/', methods=['GET'])
def list_enrollments():
    return jsonify([e.to_dict() for e in Enrollment.query.all()])


if __name__ == '__main__':
    app.run(port=5002, debug=True)
