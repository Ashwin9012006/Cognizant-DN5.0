from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

courses_db = [
    {'id': 1, 'name': 'Intro to Computer Science', 'code': 'CS101', 'credits': 4},
    {'id': 2, 'name': 'Data Structures', 'code': 'CS102', 'credits': 4}
]

def make_response_json(data, status_code=200):
    """Formats standard JSON response envelope."""
    return jsonify({'status': 'success', 'data': data}), status_code

@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_response_json(courses_db, 200)

@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    required = ['name', 'code', 'credits']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing required fields: {", ".join(missing)}'}), 400

    new_course = {
        'id': len(courses_db) + 1,
        'name': data['name'],
        'code': data['code'],
        'credits': data['credits']
    }
    courses_db.append(new_course)
    return make_response_json(new_course, 201)

@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404
    return make_response_json(course, 200)

@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404

    data = request.get_json() or {}
    course.update({k: v for k, v in data.items() if k in ['name', 'code', 'credits']})
    return make_response_json(course, 200)

@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global courses_db
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'status': 'error', 'message': f'Course with id {course_id} not found'}), 404

    courses_db = [c for c in courses_db if c['id'] != course_id]
    return jsonify({'status': 'success', 'message': f'Course {course_id} deleted successfully'}), 200
