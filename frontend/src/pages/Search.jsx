// src/pages/Search.jsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Box,
  CircularProgress,
  Chip,
  Alert,
  Paper,
} from '@mui/material';
import { flightAPI } from '../api/flights';
import { useAuth } from '../context/AuthContext';

const Search = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const params = {
      departure: searchParams.get('departure') || 'SGN',
      arrival: searchParams.get('arrival') || 'HAN',
      date: searchParams.get('date') || new Date().toISOString().split('T')[0],
      passengers: searchParams.get('passengers') || 1,
      seat_class: searchParams.get('seat_class') || 'Economy',
    };

    const fetchFlights = async () => {
      try {
        setLoading(true);
        const response = await flightAPI.search(params);
        setFlights(response.data);
        setError('');
      } catch (err) {
        setError('Không thể tìm kiếm chuyến bay');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFlights();
  }, [location.search]);

  const handleBook = (flightId) => {
    if (!user) {
      navigate('/login');
      return;
    }
    navigate(`/booking/${flightId}`);
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Kết quả tìm kiếm
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Tìm thấy {flights.length} chuyến bay
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {flights.map((flight) => (
          <Grid item xs={12} key={flight.flight_id}>
            <Card>
              <CardContent>
                <Grid container alignItems="center" spacing={2}>
                  <Grid item xs={12} md={3}>
                    <Typography variant="h6">{flight.flight_number}</Typography>
                    <Chip
                      label={flight.status}
                      color={flight.status === 'Scheduled' ? 'success' : 'warning'}
                      size="small"
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      {flight.aircraft_name}
                    </Typography>
                  </Grid>

                  <Grid item xs={6} md={2}>
                    <Typography variant="body2" color="text.secondary">
                      Khởi hành
                    </Typography>
                    <Typography variant="subtitle1">
                      {new Date(flight.departure_time).toLocaleTimeString('vi-VN')}
                    </Typography>
                    <Typography variant="body2">
                      {flight.departure_airport} - {flight.departure_city}
                    </Typography>
                  </Grid>

                  <Grid item xs={6} md={2}>
                    <Typography variant="body2" color="text.secondary">
                      Đến nơi
                    </Typography>
                    <Typography variant="subtitle1">
                      {new Date(flight.arrival_time).toLocaleTimeString('vi-VN')}
                    </Typography>
                    <Typography variant="body2">
                      {flight.arrival_airport} - {flight.arrival_city}
                    </Typography>
                  </Grid>

                  <Grid item xs={6} md={2}>
                    <Typography variant="body2" color="text.secondary">
                      Ghế trống
                    </Typography>
                    <Typography variant="body1">
                      {flight.available_seats || 0}/{flight.total_seats}
                    </Typography>
                  </Grid>

                  <Grid item xs={6} md={3}>
                    <Typography variant="h6" color="primary">
                      {flight.price?.toLocaleString('vi-VN')}đ
                    </Typography>
                    <Button
                      variant="contained"
                      color="primary"
                      fullWidth
                      onClick={() => handleBook(flight.flight_id)}
                      sx={{ mt: 1 }}
                    >
                      Đặt vé
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {flights.length === 0 && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h6">Không tìm thấy chuyến bay phù hợp</Typography>
          <Button
            variant="outlined"
            onClick={() => navigate('/')}
            sx={{ mt: 2 }}
          >
            Tìm kiếm lại
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default Search;