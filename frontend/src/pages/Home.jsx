// src/pages/Home.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Button,
  Paper,
  Grid,
  TextField,
  MenuItem,
} from '@mui/material';
import { useForm } from 'react-hook-form';

const Home = () => {
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm({
    defaultValues: {
      departure: 'SGN',   // 👈 THÊM GIÁ TRỊ MẶC ĐỊNH
      arrival: 'HAN',     // 👈 THÊM GIÁ TRỊ MẶC ĐỊNH
    }
  });

  const onSubmit = (data) => {
    const params = new URLSearchParams(data).toString();
    navigate(`/search?${params}`);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" align="center" gutterBottom>
          ✈️ Đặt vé máy bay online
        </Typography>
        <Typography variant="subtitle1" align="center" color="text.secondary">
          Giá tốt nhất, dịch vụ tốt nhất
        </Typography>
      </Box>

      <Paper elevation={3} sx={{ p: 4, maxWidth: 800, mx: 'auto' }}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                label="Điểm đi"
                select
                {...register('departure', { required: true })}
                defaultValue="SGN"  // 👈 THÊM defaultValue
              >
                <MenuItem value="SGN">Sài Gòn (SGN)</MenuItem>
                <MenuItem value="HAN">Hà Nội (HAN)</MenuItem>
                <MenuItem value="DAD">Đà Nẵng (DAD)</MenuItem>
                <MenuItem value="BKK">Bangkok (BKK)</MenuItem>
                <MenuItem value="SIN">Singapore (SIN)</MenuItem>
              </TextField>
            </Grid>

            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                label="Điểm đến"
                select
                {...register('arrival', { required: true })}
                defaultValue="HAN"  // 👈 THÊM defaultValue
              >
                <MenuItem value="SGN">Sài Gòn (SGN)</MenuItem>
                <MenuItem value="HAN">Hà Nội (HAN)</MenuItem>
                <MenuItem value="DAD">Đà Nẵng (DAD)</MenuItem>
                <MenuItem value="BKK">Bangkok (BKK)</MenuItem>
                <MenuItem value="SIN">Singapore (SIN)</MenuItem>
              </TextField>
            </Grid>

            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                type="submit"
                variant="contained"
                size="large"
                sx={{ height: '100%' }}
              >
                Tìm
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
};

export default Home;