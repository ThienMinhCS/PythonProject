import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  Avatar,
  Grid,
} from '@mui/material';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    password: '',
    confirmPassword: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (formData.password && formData.password !== formData.confirmPassword) {
      setError('Mật khẩu xác nhận không khớp');
      return;
    }

    if (formData.password && formData.password.length < 6) {
      setError('Mật khẩu phải có ít nhất 6 ký tự');
      return;
    }

    setLoading(true);
    const updateData = {
      full_name: formData.full_name,
      phone: formData.phone,
    };

    if (formData.password) {
      updateData.password = formData.password;
    }

    const result = await updateUser(updateData);
    if (result.success) {
      setMessage('Cập nhật thông tin thành công!');
      setFormData({ ...formData, password: '', confirmPassword: '' });
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" className="py-8">
      <Paper className="p-6 md:p-8 rounded-2xl shadow-xl">
        <Box className="flex items-center gap-4 mb-6">
          <Avatar
            sx={{ width: 64, height: 64, bgcolor: 'secondary.main', fontSize: 28 }}
          >
            {user?.full_name?.charAt(0)}
          </Avatar>
          <Box>
            <Typography variant="h5" className="font-bold">{user?.full_name}</Typography>
            <Typography variant="body2" className="text-gray-500">{user?.email}</Typography>
          </Box>
        </Box>

        {message && (
          <Alert severity="success" className="mb-4 rounded-xl">{message}</Alert>
        )}
        {error && (
          <Alert severity="error" className="mb-4 rounded-xl">{error}</Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Họ và tên"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Email"
                value={formData.email}
                disabled
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Số điện thoại"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Mật khẩu mới (để trống nếu không đổi)"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Xác nhận mật khẩu mới"
                type="password"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              />
            </Grid>
          </Grid>

          <Button
            fullWidth
            type="submit"
            variant="contained"
            disabled={loading}
            className="bg-airline-blue hover:bg-blue-800 text-white font-semibold py-3 rounded-xl mt-4"
          >
            {loading ? 'Đang cập nhật...' : 'Cập nhật thông tin'}
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Profile;