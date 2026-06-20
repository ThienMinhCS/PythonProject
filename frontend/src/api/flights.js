// frontend/src/api/flights.js
import api from './axios';

export const flightAPI = {
  search: (params) => api.get('/flights/search', { params }),
  getById: (id) => api.get(`/flights/${id}`),
};