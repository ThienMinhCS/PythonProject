// src/pages/BookingHistory.jsx
import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Chip,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import { bookingAPI } from '../api/bookings';

const BookingHistory = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await bookingAPI.getMyBookings();
        setBookings(response.data);
      } catch (err) {
        setError('Không thể tải lịch sử đặt vé');
      } finally {
        setLoading(false);
      }
    };
    fetchBookings();
  }, []);

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
      <Typography variant="h4" gutterBottom>
        Lịch sử đặt vé
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Có {bookings.length} đặt vé
      </Typography>

      {bookings.length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6">Chưa có đặt vé nào</Typography>
        </Paper>
      )}

      {bookings.map((booking) => (
        <Card key={booking.booking_id} sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Mã đặt vé
                </Typography>
                <Typography variant="h6">#{booking.booking_id}</Typography>
                <Chip
                  label={booking.status}
                  color={booking.status === 'Confirmed' ? 'success' : 'warning'}
                  size="small"
                />
              </Grid>

              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Chuyến bay
                </Typography>
                <Typography variant="body1">{booking.flight_number}</Typography>
                <Typography variant="body2">
                  {new Date(booking.departure_time).toLocaleString('vi-VN')}
                </Typography>
              </Grid>

              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Hành khách
                </Typography>
                {booking.passengers?.map((p, i) => (
                  <Typography key={i} variant="body2">
                    {p.full_name}
                  </Typography>
                ))}
              </Grid>

              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Tổng tiền
                </Typography>
                <Typography variant="h6" color="primary">
                  {booking.total_amount?.toLocaleString('vi-VN')}đ
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {booking.tickets?.length} vé
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      ))}
    </Container>
  );
};

export default BookingHistory;