import api from './api';

export const getPosts = async () => {
  const response = await api.get('/posts');
  return response.data;
};

export const getPost = async (id) => {
  const response = await api.get(`/posts/${id}`);
  return response.data;
};

export const getUserPosts = async () => {
  const response = await api.get('/users/me/posts');
  return response.data;
};

export const createPost = async (postData) => {
  const response = await api.post('/posts', postData);
  return response.data;
};

export const updatePost = async (id, postData) => {
  const response = await api.put(`/posts/${id}`, postData);
  return response.data;
};

export const deletePost = async (id) => {
  await api.delete(`/posts/${id}`);
};

export const searchPosts = async (query) => {
  const response = await api.post('/posts/search', { 
    query,
    limit: 5  // Request top 5 results
  });
  return response.data;
}; 