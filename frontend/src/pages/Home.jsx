import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  MenuItem,
  Button,
} from '@mui/material';
import { FlightTakeoff, FlightLand, CalendarToday, People } from '@mui/icons-material';

const airports = [
  { code: 'SGN', name: 'Sài Gòn (SGN)' },
  { code: 'HAN', name: 'Hà Nội (HAN)' },
  { code: 'DAD', name: 'Đà Nẵng (DAD)' },
  { code: 'BKK', name: 'Bangkok (BKK)' },
  { code: 'SIN', name: 'Singapore (SIN)' },
];

const Home = () => {
  const navigate = useNavigate();
  const { register, handleSubmit, watch } = useForm({
    defaultValues: {
      departure: 'SGN',     // 👈 THÊM DEFAULT
      arrival: 'HAN',       // 👈 THÊM DEFAULT
      date: new Date().toISOString().split('T')[0],
      passengers: 1,        // 👈 THÊM DEFAULT
      seat_class: 'Economy', // 👈 THÊM DEFAULT
    },
  });

  const onSubmit = (data) => {
    const params = new URLSearchParams();
    Object.entries(data).forEach(([key, value]) => {
      params.append(key, String(value));
    });
    navigate(`/search?${params.toString()}`);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-airline-navy via-airline-blue to-airline-navy py-20 md:py-32 overflow-hidden">
        <Container maxWidth="lg" className="relative z-10">
          <Box className="text-center mb-12">
            <Typography variant="h2" className="text-white font-bold text-4xl md:text-6xl">
              ✈️ Chào mừng đến với
              <span className="text-airline-gold block mt-2">Airline Viet</span>
            </Typography>
            <Typography className="text-white/80 text-lg mt-4 max-w-2xl mx-auto">
              Đặt vé máy bay online dễ dàng, nhanh chóng với giá tốt nhất
            </Typography>
          </Box>

          {/* Search Form */}
          <Paper className="max-w-4xl mx-auto p-6 md:p-8 rounded-2xl shadow-2xl bg-white/95 backdrop-blur">
            <form onSubmit={handleSubmit(onSubmit)}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={5}>
                  <TextField
                    fullWidth
                    select
                    label="Điểm đi"
                    {...register('departure')}
                    defaultValue="SGN"
                    className="bg-white rounded-lg"
                    InputProps={{
                      startAdornment: <FlightTakeoff className="text-airline-blue mr-2" />
                    }}
                  >
                    {airports.map((ap) => (
                      <MenuItem key={ap.code} value={ap.code}>
                        {ap.name}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12} md={5}>
                  <TextField
                    fullWidth
                    select
                    label="Điểm đến"
                    {...register('arrival')}
                    defaultValue="HAN"
                    className="bg-white rounded-lg"
                    InputProps={{
                      startAdornment: <FlightLand className="text-airline-blue mr-2" />
                    }}
                  >
                    {airports.map((ap) => (
                      <MenuItem key={ap.code} value={ap.code}>
                        {ap.name}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={6} md={2}>
                  <Button
                    fullWidth
                    type="submit"
                    variant="contained"
                    className="h-full bg-airline-gold hover:bg-yellow-500 text-airline-navy font-bold text-lg rounded-lg"
                    sx={{ height: 56 }}
                  >
                    Tìm
                  </Button>
                </Grid>

                <Grid item xs={6} md={3}>
                  <TextField
                    fullWidth
                    type="date"
                    label="Ngày đi"
                    {...register('date')}
                    defaultValue={new Date().toISOString().split('T')[0]}
                    InputLabelProps={{ shrink: true }}
                    className="bg-white rounded-lg"
                    InputProps={{
                      startAdornment: <CalendarToday className="text-airline-blue mr-2" />
                    }}
                  />
                </Grid>

                <Grid item xs={6} md={3}>
                  <TextField
                    fullWidth
                    select
                    label="Số hành khách"
                    {...register('passengers')}
                    defaultValue={1}
                    className="bg-white rounded-lg"
                    InputProps={{
                      startAdornment: <People className="text-airline-blue mr-2" />
                    }}
                  >
                    {[1,2,3,4,5,6,7,8,9,10].map((n) => (
                      <MenuItem key={n} value={n}>{n}</MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={6} md={3}>
                  <TextField
                    fullWidth
                    select
                    label="Hạng vé"
                    {...register('seat_class')}
                    defaultValue="Economy"
                    className="bg-white rounded-lg"
                  >
                    <MenuItem value="Economy">Economy</MenuItem>
                    <MenuItem value="Premium Economy">Premium Economy</MenuItem>
                    <MenuItem value="Business">Business</MenuItem>
                    <MenuItem value="First Class">First Class</MenuItem>
                  </TextField>
                </Grid>
              </Grid>
            </form>
          </Paper>
        </Container>
      </div>
    </div>
  );
};

export default Home;