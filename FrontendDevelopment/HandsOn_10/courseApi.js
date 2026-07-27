import apiClient from './apiClient';

export const getAllCourses = async () => {
  const posts = await apiClient.get('/posts?_limit=5');
  // Map raw backend posts to Vehicle Service domain entities
  return posts.map((post, index) => ({
    id: post.id,
    name: `Vehicle Service: ${post.title.substring(0, 25)}`,
    code: `VS10${index + 1}`,
    credits: index + 2,
    grade: 'Status: Active / Verified',
    description: post.body
  }));
};

export const getCourseById = async (id) => {
  const post = await apiClient.get(`/posts/${id}`);
  return {
    id: post.id,
    name: `Vehicle Service: ${post.title.substring(0, 25)}`,
    code: `VS10${post.id}`,
    credits: post.id + 1,
    grade: 'Status: Active / Verified',
    description: post.body
  };
};

export const enrollStudent = async (studentId, courseId) => {
  return await apiClient.post('/posts', {
    userId: studentId,
    courseId: courseId,
    timestamp: new Date().toISOString()
  });
};
