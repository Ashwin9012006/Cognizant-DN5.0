/*
===================================================================
SIDE-BY-SIDE COMPARISON: FETCH vs AXIOS
===================================================================
1. Response Parsing:
   - Fetch: Requires manual call to response.json() to parse the JSON response body.
   - Axios: Automatically parses JSON responses and provides the result in response.data.

2. HTTP Error Handling:
   - Fetch: Only rejects promises on network failures (e.g. offline). It considers 404 or 500 as success, requiring manual response.ok checks.
   - Axios: Automatically rejects the promise for any non-2xx status codes (e.g. 404, 500) and routes to .catch() / try-catch.

3. Interceptors & Convenience Features:
   - Fetch: Built directly into modern browsers, no extra library weight, but requires custom wrappers for request/response interceptors or timeouts.
   - Axios: Offers built-in request/response interceptors (e.g., axios.interceptors.request.use), request cancellation, and configurable default timeouts out of the box.
===================================================================
*/

// Sample Local Vehicle Services Data
const localCourses = [
    { id: 1, name: "Engine Oil & Filter Change", code: "VS101", credits: 4, grade: "Status: Completed (A)" },
    { id: 2, name: "Brake System Inspection", code: "VS102", credits: 3, grade: "Status: Verified (A)" },
    { id: 3, name: "Wheel Alignment & Balancing", code: "VS103", credits: 5, grade: "Status: Scheduled (B)" },
    { id: 4, name: "Transmission Service", code: "VS104", credits: 4, grade: "Status: Completed (A)" },
    { id: 5, name: "Battery & Electrical Audit", code: "VS105", credits: 2, grade: "Status: Verified (A)" }
];

// --- TASK 1: Promises and async/await ---

// Step 45: Promise chaining version of fetchUser
function fetchUserPromise(id) {
    return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
        .then(response => {
            if (!response.ok) throw new Error('User not found');
            return response.json();
        })
        .then(user => {
            console.log(`[Promise.then] User ${id} Name:`, user.name);
            return user;
        });
}

// Step 46: Async/await version of fetchUser
async function fetchUser(id) {
    try {
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
        if (!response.ok) throw new Error('User not found');
        const user = await response.json();
        console.log(`[Async/Await] User ${id} Name:`, user.name);
        return user;
    } catch (error) {
        console.error('Error fetching user:', error.message);
    }
}

// Step 47: Simulate 1-second network delay for courses
function fetchAllCourses() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(localCourses);
        }, 1000);
    });
}

// Step 48: Call fetchAllCourses with loading indicator
async function loadCoursesUI() {
    const loadingElem = document.getElementById('courses-loading');
    const gridElem = document.getElementById('courses-grid');

    loadingElem.style.display = 'flex';
    gridElem.innerHTML = '';

    const courses = await fetchAllCourses();

    loadingElem.style.display = 'none';

    courses.forEach(course => {
        const card = document.createElement('article');
        card.className = 'course-card';
        card.innerHTML = `
            <h3>${course.name}</h3>
            <p>Code: ${course.code} | Credits: ${course.credits}</p>
            <p>${course.grade}</p>
        `;
        gridElem.appendChild(card);
    });
}

// Step 49: Promise.all() demonstration
async function demonstratePromiseAll() {
    try {
        console.log('Starting Promise.all for User 1 and User 2...');
        const [user1Response, user2Response] = await Promise.all([
            fetch('https://jsonplaceholder.typicode.com/users/1').then(res => res.json()),
            fetch('https://jsonplaceholder.typicode.com/users/2').then(res => res.json())
        ]);
        console.log('Promise.all Complete -> User 1:', user1Response.name, '| User 2:', user2Response.name);
    } catch (err) {
        console.error('Promise.all error:', err);
    }
}


// --- TASK 2 & 3: Fetch API, Error Handling & Axios ---

// Step 58: Axios Request Interceptor
if (typeof axios !== 'undefined') {
    axios.interceptors.request.use(config => {
        console.log(`[Axios Interceptor] API call started: ${config.url}`);
        return config;
    }, error => {
        return Promise.reject(error);
    });
}

// Step 50 & 56: Reusable Axios-based apiFetch
async function apiFetch(url, params = {}) {
    try {
        const response = await axios.get(url, { params });
        return response.data; // Axios unwraps JSON in .data
    } catch (error) {
        const status = error.response ? error.response.status : 'Network Error';
        throw new Error(`Failed to load data (HTTP ${status})`);
    }
}

// Step 51 - 54: Load Notifications with Error Handling and Retry
async function loadNotifications(urlToFetch) {
    const loadingElem = document.getElementById('notifications-loading');
    const errorElem = document.getElementById('notifications-error');
    const errorMessageElem = document.getElementById('error-message');
    const listElem = document.getElementById('notifications-list');

    loadingElem.style.display = 'flex';
    errorElem.style.display = 'none';
    listElem.innerHTML = '';

    try {
        // Step 57: Fetch posts belonging to userId: 1 using params object
        const posts = await apiFetch(urlToFetch, { _limit: 5 });

        loadingElem.style.display = 'none';

        posts.forEach(post => {
            const card = document.createElement('article');
            card.className = 'notification-card';
            card.innerHTML = `
                <h3>Notification #${post.id}: ${post.title.substring(0, 30)}</h3>
                <p>${post.body}</p>
            `;
            listElem.appendChild(card);
        });
    } catch (err) {
        loadingElem.style.display = 'none';
        errorElem.style.display = 'flex';
        errorMessageElem.textContent = err.message;
    }
}

// Attach Retry button handler
document.getElementById('retry-btn').addEventListener('click', () => {
    // Retry with valid endpoint
    loadNotifications('https://jsonplaceholder.typicode.com/posts');
});


// Init on DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    fetchUserPromise(1);
    fetchUser(2);
    demonstratePromiseAll();
    loadCoursesUI();

    // Demonstrate initial call with valid endpoint
    loadNotifications('https://jsonplaceholder.typicode.com/posts');

    // To simulate 404 error requirement (Step 53), try calling invalid URL after 3 seconds:
    setTimeout(() => {
        console.warn('Simulating 404 Error request to show UI error handling...');
        loadNotifications('https://jsonplaceholder.typicode.com/nonexistent_endpoint');
    }, 4000);
});
