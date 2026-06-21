import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Box,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { bookingApi } from '../api/bookings';
import toast from 'react-hot-toast';

const MyBookings = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await bookingApi.getMyBookings();
        setBookings(response);
      } catch (err) {
        setError('Không thể tải lịch sử đặt vé');
        toast.error('Không thể tải lịch sử đặt vé');
      } finally {
        setLoading(false);
      }
    };
    fetchBookings();
  }, []);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
  };

  if (loading) {
    return (
      <Container className="flex justify-center items-center min-h-[60vh]">
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-8">
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" className="py-8">
      <Typography variant="h4" className="font-bold text-airline-navy mb-6">
        📋 Lịch sử đặt vé
      </Typography>

      {bookings.length === 0 ? (
        <Card className="p-12 text-center rounded-2xl">
          <Typography variant="h6" className="text-gray-500 mb-4">
            Bạn chưa có đặt vé nào
          </Typography>
          <Button variant="contained" onClick={() => navigate('/search')} className="bg-airline-blue">
            Tìm chuyến bay ngay
          </Button>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {bookings.map((booking) => (
            <Grid item xs={12} key={booking.booking_id}>
              <Card className="hover:shadow-xl transition-all duration-300 rounded-2xl">
                <CardContent className="p-6">
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={3}>
                      <Typography variant="caption" className="text-gray-500">Mã đặt vé</Typography>
                      <Typography variant="h6" className="font-bold">#{booking.booking_id}</Typography>
                      <Chip
                        label={booking.status}
                        color={booking.status === 'Confirmed' ? 'success' : 'warning'}
                        size="small"
                      />
                    </Grid>

                    <Grid item xs={12} md={3}>
                      <Typography variant="caption" className="text-gray-500">Chuyến bay</Typography>
                      <Typography variant="body1" className="font-semibold">{booking.flight_number}</Typography>
                      <Typography variant="body2">
                        {new Date(booking.departure_time).toLocaleString('vi-VN')}
                      </Typography>
                    </Grid>

                    <Grid item xs={12} md={3}>
                      <Typography variant="caption" className="text-gray-500">Hành khách</Typography>
                      {booking.passengers?.map((p, i) => (
                        <Typography key={i} variant="body2">{p.full_name}</Typography>
                      ))}
                    </Grid>

                    <Grid item xs={12} md={3}>
                      <Typography variant="caption" className="text-gray-500">Tổng tiền</Typography>
                      <Typography variant="h6" className="font-bold text-airline-blue">
                        {formatPrice(booking.total_amount)}
                      </Typography>
                      <Typography variant="caption" className="text-gray-500">
                        {booking.tickets?.length} vé
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default MyBookings;