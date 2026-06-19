// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/common/Header';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Home from './pages/Home';
import Search from './pages/Search';
import Booking from './pages/Booking';
import Profile from './pages/Profile';
import BookingHistory from './pages/BookingHistory';
import { Box, CircularProgress } from '@mui/material';

// Component bảo vệ route
const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Header />
          <Box sx={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/search" element={<Search />} />
              <Route 
                path="/booking/:flightId" 
                element={
                  <PrivateRoute>
                    <Booking />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <PrivateRoute>
                    <Profile />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/bookings" 
                element={
                  <PrivateRoute>
                    <BookingHistory />
                  </PrivateRoute>
                } 
              />
            </Routes>
          </Box>
        </Box>
        <ToastContainer position="top-right" />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;