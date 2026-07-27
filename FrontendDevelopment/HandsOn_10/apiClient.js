import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Step 141: Request interceptor attaching mock Authorization header
apiClient.interceptors.request.use(
  (config) => {
    config.headers['Authorization'] = 'Bearer mock-jwt-token-xyz123';
    console.log(`[Centralized API] Request Outgoing -> ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Step 140: Response interceptor returning response.data and standardizing errors
apiClient.interceptors.response.use(
  (response) => {
    // Return data directly so callers get response.data instead of Axios response wrapper
    return response.data;
  },
  (error) => {
    const statusCode = error.response ? error.response.status : 500;
    const message = error.response?.data?.message || error.message || 'An unexpected API error occurred';
    
    // Throw standardized Error object
    const customError = new Error(message);
    customError.statusCode = statusCode;
    return Promise.reject(customError);
  }
);

export default apiClient;
