import React from 'react';
import { Card, CardContent, Grid, Typography, Box, Chip, Button, Divider } from '@mui/material';
import { FlightTakeoff, FlightLand, EventSeat } from '@mui/icons-material'; 

const FlightCard = ({ flight, onBook }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('vi-VN', { weekday: 'short', day: 'numeric', month: 'short' });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Scheduled': return 'success';
      case 'Departed': return 'warning';
      case 'Landed': return 'info';
      case 'Cancelled': return 'error';
      default: return 'default';
    }
  };

  return (
    <Card className="hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 rounded-2xl overflow-hidden">
      <CardContent className="p-6">
        <Grid container alignItems="center" spacing={2}>
          <Grid item xs={12} md={5}>
            <Box className="flex items-center gap-4">
              <Box className="bg-airline-lightblue p-3 rounded-xl">
                <Typography variant="h6" className="font-bold text-airline-blue">
                  {flight.flight_number}
                </Typography>
              </Box>
              <Box>
                <Chip
                  label={flight.status}
                  color={getStatusColor(flight.status)}
                  size="small"
                  className="font-semibold"
                />
                <Typography variant="caption" className="block text-gray-500">
                  {flight.aircraft_name}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} md={4}>
            <Box className="flex items-center gap-3">
              <Box className="text-center">
                <Typography variant="h5" className="font-bold">{flight.departure_airport}</Typography>
                <Typography variant="body2" className="text-gray-500">{flight.departure_city}</Typography>
                <Typography variant="caption" className="text-gray-400">
                  {formatDate(flight.departure_time)} {formatTime(flight.departure_time)}
                </Typography>
              </Box>
              
              <Box className="flex-1 flex flex-col items-center px-2">
                <Typography variant="caption" className="text-gray-400">✈️</Typography>
                <Divider className="w-full" />
              </Box>
              
              <Box className="text-center">
                <Typography variant="h5" className="font-bold">{flight.arrival_airport}</Typography>
                <Typography variant="body2" className="text-gray-500">{flight.arrival_city}</Typography>
                <Typography variant="caption" className="text-gray-400">
                  {formatDate(flight.arrival_time)} {formatTime(flight.arrival_time)}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} md={3}>
            <Box className="text-center">
              <Typography variant="h5" className="font-bold text-airline-blue">
                {formatPrice(flight.price)}
              </Typography>
              <Box className="flex items-center justify-center gap-2 text-sm text-gray-500">
                <Seat fontSize="small" />
                <Typography variant="caption">
                  {flight.available_seats} ghế trống
                </Typography>
              </Box>
              <Button
                variant="contained"
                fullWidth
                onClick={() => onBook(flight.flight_id)}
                disabled={flight.available_seats === 0}
                className="mt-2 bg-airline-blue hover:bg-blue-800 text-white font-semibold rounded-lg py-2"
              >
                {flight.available_seats === 0 ? 'Hết ghế' : 'Đặt vé'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default FlightCard;