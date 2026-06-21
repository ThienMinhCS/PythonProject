import React, { createContext, useState, useContext, useEffect } from 'react';
import { authApi } from '../api/auth';
import toast from 'react-hot-toast';

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
      } catch {
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (data) => {
    try {
      const result = await authApi.login(data);
      const { access_token, user } = result;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);
      toast.success('🎉 Đăng nhập thành công!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Đăng nhập thất bại';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const register = async (data) => {
    try {
      const result = await authApi.register(data);
      const { access_token, user } = result;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);
      toast.success('🎉 Đăng ký thành công!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Đăng ký thất bại';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    toast.success('Đã đăng xuất');
  };

  const updateUser = async (data) => {
    try {
      const updated = await authApi.updateMe(data);
      localStorage.setItem('user', JSON.stringify(updated));
      setUser(updated);
      toast.success('✅ Cập nhật thành công!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Cập nhật thất bại';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        updateUser,
        isAuthenticated: !!user,
        isAdmin: user?.role === 'Admin',
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};