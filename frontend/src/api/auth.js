// src/api/auth.js
import api from './axios';

export const authApi = {
  login: async (data) => {
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);
    
    const response = await api.post('/auth/login', formData, {  // 👈 Bỏ /api/v1
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  register: async (data) => {
    const response = await api.post('/auth/register', data);  // 👈 Bỏ /api/v1
    return response.data;
  },

  getMe: async () => {
    const response = await api.get('/users/me');  // 👈 Bỏ /api/v1
    return response.data;
  },

  updateMe: async (data) => {
    const response = await api.put('/users/me', data);  // 👈 Bỏ /api/v1
    return response.data;
  },
};