import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Container, Paper, TextField, Button, Typography, Box, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Register = () => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Mật khẩu xác nhận không khớp');
      return;
    }

    if (formData.password.length < 6) {
      setError('Mật khẩu phải có ít nhất 6 ký tự');
      return;
    }

    setLoading(true);
    const { confirmPassword, ...registerData } = formData;
    const result = await register(registerData);

    if (!result.success) {
      setError(result.error || 'Đăng ký thất bại');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm" className="py-8">
      <Paper className="p-8 rounded-2xl shadow-2xl">
        <Box className="text-center mb-6">
          <Typography variant="h4" className="font-bold text-airline-navy">
            ✈️ Tạo tài khoản
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" className="mb-4 rounded-xl">
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Họ và tên"
            required
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            className="mb-4"
          />

          <TextField
            fullWidth
            label="Email"
            type="email"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="mb-4"
          />

          <TextField
            fullWidth
            label="Số điện thoại"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            className="mb-4"
          />

          <TextField
            fullWidth
            label="Mật khẩu"
            type="password"
            required
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="mb-4"
          />

          <TextField
            fullWidth
            label="Xác nhận mật khẩu"
            type="password"
            required
            value={formData.confirmPassword}
            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
            className="mb-6"
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            className="bg-airline-blue hover:bg-blue-800 text-white font-semibold py-3 rounded-xl"
          >
            {loading ? 'Đang đăng ký...' : 'Đăng ký'}
          </Button>
        </form>

        <Box className="mt-4 text-center">
          <Typography variant="body2" className="text-gray-500">
            Đã có tài khoản?{' '}
            <Link to="/login" className="text-airline-blue font-semibold hover:underline">
              Đăng nhập ngay
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;