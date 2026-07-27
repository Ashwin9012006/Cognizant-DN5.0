import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

export default function ProfilePage() {
  const dispatch = useDispatch();
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  const handleUnenroll = (id) => {
    dispatch(unenroll(id));
  };

  const totalCredits = enrolledCourses.reduce((sum, item) => sum + item.credits, 0);

  return (
    <div>
      <h2>Vehicle Owner & Profile Overview</h2>
      <div className="detail-card" style={{ marginTop: '1rem' }}>
        <p><strong>Owner Name:</strong> Jane Doe</p>
        <p><strong>Email:</strong> jane.doe@vehicleservice.com</p>
        <p><strong>Service Interval:</strong> Cycle 6</p>
        <p><strong>Total Enrolled Credits/Hours:</strong> {totalCredits}</p>
      </div>

      <h3 style={{ marginTop: '2rem', color: '#0f172a' }}>Booked Vehicle Services</h3>
      {enrolledCourses.length === 0 ? (
        <p style={{ marginTop: '0.5rem', color: '#64748b' }}>No vehicle services booked yet.</p>
      ) : (
        <ul className="enrolled-list">
          {enrolledCourses.map(item => (
            <li key={item.id} className="enrolled-item">
              <div>
                <strong>{item.code} — {item.name}</strong> ({item.credits} Credits)
              </div>
              <button className="btn-danger" onClick={() => handleUnenroll(item.id)}>
                Cancel Booking
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
