// src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../api/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      console.log('🔐 Login attempt:', email);
      const response = await authAPI.login({ email, password });
      console.log('✅ Login response:', response.data);
      
      const { access_token, user } = response.data;
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);
      
      return { success: true, user };
    } catch (error) {
      console.error('❌ Login error:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Đăng nhập thất bại' 
      };
    }
  };

  const register = async (userData) => {
    try {
      console.log('📝 Register attempt:', userData.email);
      const response = await authAPI.register(userData);
      console.log('✅ Register response:', response.data);
      
      const { access_token, user } = response.data;
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);
      
      return { success: true, user };
    } catch (error) {
      console.error('❌ Register error:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Đăng ký thất bại' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const updateUser = async (data) => {
    try {
      const response = await authAPI.updateMe(data);
      const updatedUser = response.data;
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setUser(updatedUser);
      return { success: true, user: updatedUser };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Cập nhật thất bại' 
      };
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export default AuthContext;