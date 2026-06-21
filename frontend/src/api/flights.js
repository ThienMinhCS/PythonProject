// src/api/flights.js
import api from './axios';

export const flightApi = {
  search: async (params) => {
    const response = await api.get('/flights/search', { params });  // 👈 Bỏ /api/v1
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/flights/${id}`);  // 👈 Bỏ /api/v1
    return response.data;
  },
};