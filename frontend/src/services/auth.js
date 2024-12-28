import api from './api';

export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await api.post('/users/login', formData);
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/users', userData);
  return response.data;
};

export const getUserProfile = async () => {
  const response = await api.get('/users/me');
  return response.data;
};

export const updatePassword = async (passwordData) => {
  const response = await api.put('/users/me', passwordData);
  return response.data;
}; 