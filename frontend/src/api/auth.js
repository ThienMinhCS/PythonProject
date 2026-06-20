//frontend/src/api/auth.js
import api from './axios';

export const authAPI = {
  // Đăng nhập - dùng form data
  login: (data) => {
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  
  // Đăng ký
  register: (data) => api.post('/auth/register', data),
  
  // Lấy thông tin user
  getMe: () => api.get('/users/me'),
  
  // Cập nhật user
  updateMe: (data) => api.put('/users/me', data),
};