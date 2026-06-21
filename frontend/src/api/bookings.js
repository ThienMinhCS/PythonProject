// src/api/bookings.js
import api from './axios';

export const bookingApi = {
  create: async (data) => {
    const response = await api.post('/bookings/', data);  // 👈 Bỏ /api/v1
    return response.data;
  },

  getMyBookings: async () => {
    const response = await api.get('/bookings/my-bookings');  // 👈 Bỏ /api/v1
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/bookings/${id}`);  // 👈 Bỏ /api/v1
    return response.data;
  },
};