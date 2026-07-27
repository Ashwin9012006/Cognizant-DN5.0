import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { coursesData } from '../data/courses';

export default function CoursesPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  const handleEnroll = (course) => {
    dispatch(enroll(course));
    navigate('/profile'); // Step 80: Navigate user to /profile automatically after enrolling
  };

  return (
    <div>
      <h2>Available Vehicle Services</h2>
      <div className="grid">
        {coursesData.map(course => {
          const isEnrolled = enrolledCourses.some(item => item.id === course.id);
          return (
            <div key={course.id} className="card">
              <div>
                <div className="code">{course.code}</div>
                <h3>{course.name}</h3>
                <p>{course.description}</p>
                <p><strong>Credits/Hours:</strong> {course.credits}</p>
              </div>
              <div className="card-actions">
                <Link to={`/courses/${course.id}`} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                  View Details
                </Link>
                <button
                  className="btn-primary"
                  style={{ backgroundColor: isEnrolled ? '#94a3b8' : '#2563eb' }}
                  disabled={isEnrolled}
                  onClick={() => handleEnroll(course)}
                >
                  {isEnrolled ? 'Enrolled' : 'Enroll'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
