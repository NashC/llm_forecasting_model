import api from './api';

export const loginUser = async (email, password) => {
  // API expects username and password for login endpoint
  const formData = new FormData();
  formData.append('username', email);  // Backend expects 'username' field but we use email
  formData.append('password', password);

  const response = await api.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};

export const registerUser = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/users/me');
  return response.data;
};

export const refreshToken = async (refreshToken) => {
  const response = await api.post('/auth/refresh', { refresh_token: refreshToken });
  return response.data;
};

export const updateUserProfile = async (userData) => {
  const response = await api.put('/users/me', userData);
  return response.data;
}; 