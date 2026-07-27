import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';

export default function App() {
  const [courses, setCourses] = useState([]);
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Step 71 - 73: Fetch initial courses from API with loading and error handling
  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network error: Unable to fetch vehicle services.');
        }
        return response.json();
      })
      .then(data => {
        // Map posts to vehicle service course-like objects
        const mappedCourses = data.map((item, index) => ({
          id: item.id,
          name: `Vehicle Service: ${item.title.substring(0, 25)}`,
          code: `VS10${index + 1}`,
          credits: index + 2,
          grade: 'Status: Active'
        }));
        setCourses(mappedCourses);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []); // Empty dependency array means this effect runs once on component mount (equivalent to componentDidMount)

  /*
    Step 75: useEffect with [courses] dependency array.
    Why the dependency array matters:
    - An empty array [] runs the effect once after initial render.
    - Providing [courses] ensures the callback executes ONLY when the `courses` state reference changes.
    - Omitting the dependency array entirely would cause the effect to run on EVERY render, which could
      lead to performance issues or infinite loops if the effect updates state.
  */
  useEffect(() => {
    if (courses.length > 0) {
      console.log('Courses updated:', courses);
    }
  }, [courses]);

  // Step 69: Lifting state up for course enrollment
  const handleEnroll = (course) => {
    if (!enrolledCourses.some(c => c.id === course.id)) {
      setEnrolledCourses(prev => [...prev, course]);
    }
  };

  // Step 68: Filter displayed courses based on searchTerm
  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app">
      <Header siteName="Vehicle Service Portal" enrolledCount={enrolledCourses.length} />

      <main className="container" id="services">
        <h2>Available Vehicle Services</h2>

        <div className="controls">
          <input
            type="text"
            className="search-input"
            placeholder="Search vehicle services by name or code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {loading && <div className="loading">Loading services...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && !error && (
          <div className="grid">
            {filteredCourses.map(course => (
              <CourseCard
                key={course.id}
                {...course}
                isEnrolled={enrolledCourses.some(c => c.id === course.id)}
                onEnroll={handleEnroll}
              />
            ))}
          </div>
        )}

        <StudentProfile />
      </main>

      <Footer />
    </div>
  );
}
