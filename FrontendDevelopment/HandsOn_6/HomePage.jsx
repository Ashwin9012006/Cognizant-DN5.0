import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="hero-box">
      <h2>Welcome to Vehicle Service Portal</h2>
      <p>Streamline your vehicle maintenance, browse available service packages, and manage your bookings in real time.</p>
      <Link to="/courses" className="btn-primary">Browse Services</Link>
    </div>
  );
}
