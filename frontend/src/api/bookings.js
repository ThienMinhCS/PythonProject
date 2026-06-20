// frontend/src/api/bookings.js
import api from './axios';

export const bookingAPI = {
  create: (data) => api.post('/bookings/', data),
  getMyBookings: () => api.get('/bookings/my-bookings'),
  getById: (id) => api.get(`/bookings/${id}`),
};