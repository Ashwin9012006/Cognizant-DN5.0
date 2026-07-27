import { courses } from './data.js';

// Copy of courses for manipulating layout/sorting
let courseList = [...courses];

// Task 1: ES6+ Syntax Practice
const logCoursePractice = () => {
    // Destructuring in loop
    courses.forEach(course => {
        const { name, credits } = course;
        // console.log(`Service: ${name}, Credits: ${credits}`);
    });

    // Array.map()
    const formattedCourses = courses.map(c => `${c.code} — ${c.name} (${c.credits} credits)`);
    console.log('Formatted Courses:', formattedCourses);

    // Array.filter() for credits >= 4
    const highCreditCourses = courses.filter(c => c.credits >= 4);
    console.log('High Credit Count (>=4):', highCreditCourses.length);

    // Array.reduce() for total credits
    const totalCreditsSum = courses.reduce((sum, c) => sum + c.credits, 0);
    console.log('Total Enrolled Credits:', totalCreditsSum);
};

// Task 2: DOM Selection & Dynamic Rendering
const gridContainer = document.querySelector('.course-grid');
const totalCreditsElem = document.getElementById('total-credits');
const selectedCourseElem = document.getElementById('selected-course');
const searchInput = document.getElementById('search-courses');
const sortBtn = document.getElementById('sort-credits');

const renderGrid = (items) => {
    gridContainer.innerHTML = '';

    const fragment = document.createDocumentFragment();

    items.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.dataset.id = course.id;

        article.innerHTML = `
            <div>
                <div class="code">${course.code}</div>
                <h3>${course.name}</h3>
                <p>Comprehensive maintenance for vehicle safety and performance.</p>
            </div>
            <div class="meta">
                <span class="credits">${course.credits} Credits</span>
                <span class="grade">${course.grade}</span>
            </div>
        `;

        fragment.appendChild(article);
    });

    gridContainer.appendChild(fragment);

    // Update total credits dynamically
    const total = items.reduce((sum, c) => sum + c.credits, 0);
    totalCreditsElem.textContent = `Total Credits: ${total}`;
};

// Task 3: Event Listeners & Interactivity
// Search input filtering (case-insensitive)
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase().trim();
    const filtered = courseList.filter(c => c.name.toLowerCase().includes(term) || c.code.toLowerCase().includes(term));
    renderGrid(filtered);
});

// Sort by Credits descending
sortBtn.addEventListener('click', () => {
    courseList.sort((a, b) => b.credits - a.credits);
    renderGrid(courseList);
});

// Event Delegation on course-grid container
gridContainer.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (card) {
        const cardId = parseInt(card.dataset.id, 10);
        const selected = courseList.find(c => c.id === cardId);
        if (selected) {
            selectedCourseElem.textContent = `Selected: ${selected.name} (${selected.code}) - ${selected.grade}`;
        }
    }
});

// Initialize on page load
logCoursePractice();
renderGrid(courseList);
