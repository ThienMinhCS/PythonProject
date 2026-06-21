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
  Card,
  CardContent,
  Chip,
  IconButton,
} from '@mui/material';
import { Delete, Add, FlightTakeoff, FlightLand } from '@mui/icons-material';
import { flightApi } from '../api/flights';
import { bookingApi } from '../api/bookings';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const steps = ['Thông tin chuyến bay', 'Thông tin hành khách', 'Xác nhận'];

const Booking = () => {
  const { flightId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [activeStep, setActiveStep] = useState(0);
  const [flight, setFlight] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [seatClass, setSeatClass] = useState('Economy');
  const [bookingResult, setBookingResult] = useState(null);
  
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

  useEffect(() => {
    const fetchFlight = async () => {
      try {
        const response = await flightApi.getById(parseInt(flightId));
        setFlight(response);
      } catch (err) {
        setError('Không thể tải thông tin chuyến bay');
        toast.error('Không thể tải thông tin chuyến bay');
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
      const response = await bookingApi.create(bookingData);
      setBookingResult(response);
      setActiveStep(2);
      toast.success('🎉 Đặt vé thành công!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Đặt vé thất bại';
      setError(msg);
      toast.error(msg);
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

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
  };

  if (loading && activeStep < 2) {
    return (
      <Container className="flex justify-center items-center min-h-[60vh]">
        <CircularProgress />
      </Container>
    );
  }

  if (error && activeStep < 2) {
    return (
      <Container className="py-8">
        <Alert severity="error" className="rounded-xl">{error}</Alert>
        <Button variant="outlined" onClick={() => navigate('/search')} className="mt-4">
          Quay lại tìm kiếm
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" className="py-8">
      <Paper className="p-6 md:p-8 rounded-2xl shadow-xl">
        <Typography variant="h4" className="font-bold text-airline-navy mb-2">
          ✈️ Đặt vé
        </Typography>

        <Stepper activeStep={activeStep} className="mb-8">
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {activeStep === 0 && flight && (
          <Box>
            <Typography variant="h6" className="font-semibold mb-4">Thông tin chuyến bay</Typography>
            <Card className="bg-airline-lightblue/30 rounded-xl">
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Box className="flex items-center gap-2">
                      <FlightTakeoff className="text-airline-blue" />
                      <Box>
                        <Typography variant="caption" className="text-gray-500">Khởi hành</Typography>
                        <Typography variant="body1" className="font-semibold">
                          {flight.departure_airport} - {flight.departure_city}
                        </Typography>
                        <Typography variant="body2">
                          {new Date(flight.departure_time).toLocaleString('vi-VN')}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Box className="flex items-center gap-2">
                      <FlightLand className="text-airline-blue" />
                      <Box>
                        <Typography variant="caption" className="text-gray-500">Đến nơi</Typography>
                        <Typography variant="body1" className="font-semibold">
                          {flight.arrival_airport} - {flight.arrival_city}
                        </Typography>
                        <Typography variant="body2">
                          {new Date(flight.arrival_time).toLocaleString('vi-VN')}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      select
                      label="Hạng ghế"
                      fullWidth
                      value={seatClass}
                      onChange={(e) => setSeatClass(e.target.value)}
                    >
                      <MenuItem value="Economy">Economy - {formatPrice(flight.price)}</MenuItem>
                      <MenuItem value="Premium Economy">Premium Economy</MenuItem>
                      <MenuItem value="Business">Business</MenuItem>
                      <MenuItem value="First Class">First Class</MenuItem>
                    </TextField>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Box>
        )}

        {activeStep === 1 && (
          <Box>
            <Box className="flex items-center justify-between mb-4">
              <Typography variant="h6" className="font-semibold">
                Thông tin hành khách ({passengers.length} người)
              </Typography>
              <Button startIcon={<Add />} onClick={addPassenger} variant="outlined" size="small">
                Thêm hành khách
              </Button>
            </Box>

            {passengers.map((passenger, index) => (
              <Card key={index} className="mb-4 bg-gray-50 rounded-xl">
                <CardContent>
                  <Box className="flex items-center justify-between mb-3">
                    <Typography variant="subtitle1" className="font-semibold">
                      Hành khách {index + 1}
                    </Typography>
                    {passengers.length > 1 && (
                      <IconButton size="small" color="error" onClick={() => removePassenger(index)}>
                        <Delete />
                      </IconButton>
                    )}
                  </Box>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Họ và tên"
                        required
                        value={passenger.full_name}
                        onChange={(e) => updatePassenger(index, 'full_name', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        select
                        label="Giới tính"
                        value={passenger.gender}
                        onChange={(e) => updatePassenger(index, 'gender', e.target.value)}
                      >
                        <MenuItem value="Male">Nam</MenuItem>
                        <MenuItem value="Female">Nữ</MenuItem>
                        <MenuItem value="Other">Khác</MenuItem>
                      </TextField>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        type="date"
                        label="Ngày sinh"
                        InputLabelProps={{ shrink: true }}
                        value={passenger.date_of_birth}
                        onChange={(e) => updatePassenger(index, 'date_of_birth', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Quốc tịch"
                        value={passenger.nationality}
                        onChange={(e) => updatePassenger(index, 'nationality', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        select
                        label="Loại giấy tờ"
                        value={passenger.identifier_type}
                        onChange={(e) => updatePassenger(index, 'identifier_type', e.target.value)}
                      >
                        <MenuItem value="Passport">Hộ chiếu</MenuItem>
                        <MenuItem value="ID Card">CMND/CCCD</MenuItem>
                        <MenuItem value="Driver License">Bằng lái xe</MenuItem>
                      </TextField>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Số giấy tờ"
                        value={passenger.identifier_number}
                        onChange={(e) => updatePassenger(index, 'identifier_number', e.target.value)}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}

        {activeStep === 2 && bookingResult && (
          <Box>
            <Alert severity="success" className="mb-6 rounded-xl">
              🎉 Đặt vé thành công! Mã đặt vé: #{bookingResult.booking_id}
            </Alert>

            <Typography variant="h6" className="font-semibold mb-4">Chi tiết đặt vé</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card className="bg-gray-50">
                  <CardContent>
                    <Typography variant="caption" className="text-gray-500">Mã đặt vé</Typography>
                    <Typography variant="h6" className="font-bold text-airline-blue">
                      #{bookingResult.booking_id}
                    </Typography>
                    <Typography variant="caption" className="text-gray-500 block mt-2">Trạng thái</Typography>
                    <Chip label={bookingResult.status} color="success" />
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card className="bg-gray-50">
                  <CardContent>
                    <Typography variant="caption" className="text-gray-500">Tổng tiền</Typography>
                    <Typography variant="h5" className="font-bold text-airline-blue">
                      {formatPrice(bookingResult.total_amount)}
                    </Typography>
                    <Typography variant="caption" className="text-gray-500 block mt-2">Số vé</Typography>
                    <Typography>{bookingResult.tickets?.length || 0} vé</Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box className="flex gap-3 mt-6 flex-wrap">
              <Button variant="contained" onClick={() => navigate('/bookings')} className="bg-airline-blue">
                Lịch sử đặt vé
              </Button>
              <Button variant="outlined" onClick={() => navigate('/')}>
                Về trang chủ
              </Button>
            </Box>
          </Box>
        )}

        {activeStep < 2 && (
          <Box className="flex justify-between mt-6">
            <Button disabled={activeStep === 0} onClick={handleBack} variant="outlined">
              Quay lại
            </Button>
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={loading}
              className="bg-airline-blue hover:bg-blue-800"
            >
              {loading ? 'Đang xử lý...' : activeStep === 1 ? 'Xác nhận đặt vé' : 'Tiếp theo'}
            </Button>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Booking;