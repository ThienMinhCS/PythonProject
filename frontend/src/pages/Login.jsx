import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Container, Paper, TextField, Button, Typography, Box, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login({ email, password });
    
    if (!result.success) {
      setError(result.error || 'Đăng nhập thất bại');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm" className="py-12">
      <Paper className="p-8 rounded-2xl shadow-2xl">
        <Box className="text-center mb-8">
          <Typography variant="h4" className="font-bold text-airline-navy">
            ✈️ Chào mừng trở lại
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
            label="Email"
            type="email"
            margin="normal"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-4"
          />

          <TextField
            fullWidth
            label="Mật khẩu"
            type="password"
            margin="normal"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
            {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
          </Button>
        </form>

        <Box className="mt-4 text-center">
          <Typography variant="body2" className="text-gray-500">
            Chưa có tài khoản?{' '}
            <Link to="/register" className="text-airline-blue font-semibold hover:underline">
              Đăng ký ngay
            </Link>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;