// frontend/src/pages/Booking.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Box,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress,
  MenuItem,
} from '@mui/material';
import { flightAPI } from '../api/flights';
import { bookingAPI } from '../api/bookings';
import { useAuth } from '../context/AuthContext';

const steps = ['Thông tin chuyến bay', 'Thông tin hành khách', 'Xác nhận'];

const Booking = () => {
  const { flightId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [activeStep, setActiveStep] = useState(0);
  const [flight, setFlight] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [passengers, setPassengers] = useState([
    {
      full_name: '',
      gender: 'Male',
      date_of_birth: '',
      nationality: 'Vietnamese',
      identifier_type: 'Passport',
      identifier_number: '',
    },
  ]);
  const [seatClass, setSeatClass] = useState('Economy');
  const [bookingResult, setBookingResult] = useState(null);

  useEffect(() => {
    const fetchFlight = async () => {
      try {
        const response = await flightAPI.getById(flightId);
        setFlight(response.data);
      } catch (err) {
        setError('Không thể tải thông tin chuyến bay');
      } finally {
        setLoading(false);
      }
    };
    fetchFlight();
  }, [flightId]);

  const handleNext = () => {
    if (activeStep === 0) {
      setActiveStep(1);
    } else if (activeStep === 1) {
      handleBooking();
    }
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleBooking = async () => {
    try {
      setLoading(true);
      const bookingData = {
        flight_id: parseInt(flightId),
        seat_class: seatClass,
        passengers: passengers,
      };
      const response = await bookingAPI.create(bookingData);
      setBookingResult(response.data);
      setActiveStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'Đặt vé thất bại');
    } finally {
      setLoading(false);
    }
  };

  const addPassenger = () => {
    setPassengers([
      ...passengers,
      {
        full_name: '',
        gender: 'Male',
        date_of_birth: '',
        nationality: 'Vietnamese',
        identifier_type: 'Passport',
        identifier_number: '',
      },
    ]);
  };

  const removePassenger = (index) => {
    if (passengers.length > 1) {
      setPassengers(passengers.filter((_, i) => i !== index));
    }
  };

  const updatePassenger = (index, field, value) => {
    const updated = [...passengers];
    updated[index][field] = value;
    setPassengers(updated);
  };

  if (loading && activeStep < 2) {
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
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Đặt vé
        </Typography>

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {activeStep === 0 && flight && (
          <Box>
            <Typography variant="h6">Thông tin chuyến bay</Typography>
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Mã chuyến bay
                </Typography>
                <Typography variant="body1">{flight.flight_number}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Hạng ghế
                </Typography>
                <TextField
                  select
                  fullWidth
                  size="small"
                  value={seatClass}
                  onChange={(e) => setSeatClass(e.target.value)}
                >
                  <MenuItem value="Economy">Economy</MenuItem>
                  <MenuItem value="Premium Economy">Premium Economy</MenuItem>
                  <MenuItem value="Business">Business</MenuItem>
                  <MenuItem value="First Class">First Class</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Khởi hành
                </Typography>
                <Typography variant="body1">
                  {new Date(flight.departure_time).toLocaleString('vi-VN')}
                </Typography>
                <Typography variant="body2">
                  {flight.departure_airport} - {flight.departure_city}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Đến nơi
                </Typography>
                <Typography variant="body1">
                  {new Date(flight.arrival_time).toLocaleString('vi-VN')}
                </Typography>
                <Typography variant="body2">
                  {flight.arrival_airport} - {flight.arrival_city}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary">
                  Máy bay
                </Typography>
                <Typography variant="body1">{flight.aircraft_name}</Typography>
              </Grid>
            </Grid>
          </Box>
        )}

        {activeStep === 1 && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Thông tin hành khách
            </Typography>
            {passengers.map((passenger, index) => (
              <Paper key={index} sx={{ p: 3, mb: 3, bgcolor: '#f5f5f5' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Hành khách {index + 1}
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Họ và tên"
                      required
                      value={passenger.full_name}
                      onChange={(e) =>
                        updatePassenger(index, 'full_name', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      select
                      label="Giới tính"
                      value={passenger.gender}
                      onChange={(e) =>
                        updatePassenger(index, 'gender', e.target.value)
                      }
                    >
                      <MenuItem value="Male">Nam</MenuItem>
                      <MenuItem value="Female">Nữ</MenuItem>
                      <MenuItem value="Other">Khác</MenuItem>
                    </TextField>
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      type="date"
                      label="Ngày sinh"
                      InputLabelProps={{ shrink: true }}
                      value={passenger.date_of_birth}
                      onChange={(e) =>
                        updatePassenger(index, 'date_of_birth', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Quốc tịch"
                      value={passenger.nationality}
                      onChange={(e) =>
                        updatePassenger(index, 'nationality', e.target.value)
                      }
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      select
                      label="Loại giấy tờ"
                      value={passenger.identifier_type}
                      onChange={(e) =>
                        updatePassenger(index, 'identifier_type', e.target.value)
                      }
                    >
                      <MenuItem value="Passport">Hộ chiếu</MenuItem>
                      <MenuItem value="ID Card">CMND/CCCD</MenuItem>
                      <MenuItem value="Driver License">Bằng lái xe</MenuItem>
                    </TextField>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Số giấy tờ"
                      value={passenger.identifier_number}
                      onChange={(e) =>
                        updatePassenger(index, 'identifier_number', e.target.value)
                      }
                    />
                  </Grid>
                </Grid>
                {passengers.length > 1 && (
                  <Button
                    color="error"
                    size="small"
                    onClick={() => removePassenger(index)}
                    sx={{ mt: 1 }}
                  >
                    Xóa hành khách
                  </Button>
                )}
              </Paper>
            ))}
            <Button variant="outlined" onClick={addPassenger} sx={{ mt: 1 }}>
              + Thêm hành khách
            </Button>
          </Box>
        )}

        {activeStep === 2 && bookingResult && (
          <Box>
            <Alert severity="success" sx={{ mb: 3 }}>
              Đặt vé thành công!
            </Alert>
            <Typography variant="h6">Thông tin đặt vé</Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Mã đặt vé
                </Typography>
                <Typography variant="body1">{bookingResult.booking_id}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Tổng tiền
                </Typography>
                <Typography variant="h6" color="primary">
                  {bookingResult.total_amount?.toLocaleString('vi-VN')}đ
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary">
                  Số vé
                </Typography>
                {bookingResult.tickets?.map((ticket, i) => (
                  <Typography key={i} variant="body1">
                    {ticket}
                  </Typography>
                ))}
              </Grid>
            </Grid>
            <Button
              variant="contained"
              onClick={() => navigate('/bookings')}
              sx={{ mt: 3 }}
            >
              Xem lịch sử đặt vé
            </Button>
          </Box>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
          <Button disabled={activeStep === 0} onClick={handleBack}>
            Quay lại
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={loading}
          >
            {loading ? 'Đang xử lý...' : activeStep === 2 ? 'Hoàn tất' : 'Tiếp theo'}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Booking;