import React from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { coursesData } from '../data/courses';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  const course = coursesData.find(c => c.id === parseInt(courseId, 10));

  if (!course) {
    return (
      <div className="detail-card">
        <h2>Service Not Found</h2>
        <p>No vehicle service package matches ID: {courseId}</p>
        <Link to="/courses" className="btn-primary" style={{ marginTop: '1rem' }}>Back to Services</Link>
      </div>
    );
  }

  const isEnrolled = enrolledCourses.some(item => item.id === course.id);

  const handleEnroll = () => {
    dispatch(enroll(course));
    navigate('/profile');
  };

  return (
    <div className="detail-card">
      <div className="code">{course.code}</div>
      <h2>{course.name}</h2>
      <p>{course.description}</p>

      <div className="meta-info">
        <p><strong>Credits / Duration:</strong> {course.credits} Hours</p>
        <p><strong>Service Status:</strong> {course.grade}</p>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
        <button
          className="btn-primary"
          disabled={isEnrolled}
          style={{ backgroundColor: isEnrolled ? '#94a3b8' : '#2563eb' }}
          onClick={handleEnroll}
        >
          {isEnrolled ? 'Service Booked' : 'Book / Enroll Service'}
        </button>
        <Link to="/courses" className="btn-primary" style={{ backgroundColor: '#64748b' }}>
          Back to List
        </Link>
      </div>
    </div>
  );
}
