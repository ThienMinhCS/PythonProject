// src/pages/SearchFlights.jsx
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Box,
  CircularProgress,
  Alert,
  Paper,
  Button,
  Chip,
  Slider,
  FormControlLabel,
  Switch,
} from '@mui/material';
import { FlightTakeoff, FlightLand, CalendarToday, AttachMoney } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { flightApi } from '../api/flights';
import FlightCard from '../components/flights/FlightCard';

const SearchFlights = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [flights, setFlights] = useState([]);
  const [filteredFlights, setFilteredFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [priceRange, setPriceRange] = useState([0, 10000000]);
  const [maxPrice, setMaxPrice] = useState(10000000);
  const [showOnlyAvailable, setShowOnlyAvailable] = useState(false);
  const [sortBy, setSortBy] = useState('price');

  const searchParams = new URLSearchParams(location.search);
  const departure = searchParams.get('departure') || 'SGN';
  const arrival = searchParams.get('arrival') || 'HAN';
  const date = searchParams.get('date') || new Date().toISOString().split('T')[0];
  const passengers = parseInt(searchParams.get('passengers') || '1');
  const seatClass = searchParams.get('seat_class') || 'Economy';

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true);
        const response = await flightApi.search({
          departure,
          arrival,
          date,
          passengers,
          seat_class: seatClass,
        });
        setFlights(response);
        
        if (response.length > 0) {
          const max = Math.max(...response.map(f => f.price));
          setMaxPrice(max);
          setPriceRange([0, max]);
        }
        
        setError('');
      } catch (err) {
        setError(err.response?.data?.detail || 'Không thể tìm kiếm chuyến bay');
      } finally {
        setLoading(false);
      }
    };

    fetchFlights();
  }, [location.search]);

  useEffect(() => {
    let filtered = [...flights];
    filtered = filtered.filter(f => f.price >= priceRange[0] && f.price <= priceRange[1]);
    if (showOnlyAvailable) {
      filtered = filtered.filter(f => f.available_seats > 0);
    }
    filtered.sort((a, b) => {
      if (sortBy === 'price') return a.price - b.price;
      if (sortBy === 'time') {
        return new Date(a.departure_time).getTime() - new Date(b.departure_time).getTime();
      }
      return 0;
    });
    setFilteredFlights(filtered);
  }, [flights, priceRange, showOnlyAvailable, sortBy]);

  const handleBook = (flightId) => {
    if (!user) {
      navigate('/login');
      return;
    }
    navigate(`/booking/${flightId}`);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
  };

  if (loading) {
    return (
      <Container className="flex justify-center items-center min-h-[60vh]">
        <Box className="text-center">
          <CircularProgress size={60} className="text-airline-blue" />
          <Typography className="mt-4 text-gray-500">Đang tìm kiếm chuyến bay...</Typography>
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-8">
        <Alert severity="error" className="rounded-xl">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" className="py-8">
      {/* Search Summary */}
      <Paper className="p-6 mb-6 rounded-2xl bg-gradient-to-r from-airline-navy to-airline-blue text-white">
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box className="flex items-center gap-6">
              <Box>
                <Typography variant="body2" className="text-white/70">Điểm đi</Typography>
                <Box className="flex items-center gap-2">
                  <FlightTakeoff />
                  <Typography variant="h5" className="font-bold">{departure}</Typography>
                </Box>
              </Box>
              <Typography variant="h6" className="text-airline-gold">→</Typography>
              <Box>
                <Typography variant="body2" className="text-white/70">Điểm đến</Typography>
                <Box className="flex items-center gap-2">
                  <FlightLand />
                  <Typography variant="h5" className="font-bold">{arrival}</Typography>
                </Box>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box className="flex flex-wrap gap-4 items-center justify-end">
              <Chip
                icon={<CalendarToday />}
                label={new Date(date).toLocaleDateString('vi-VN')}
                className="bg-white/20 text-white"
              />
              <Chip
                label={`${passengers} hành khách`}
                className="bg-white/20 text-white"
              />
              <Chip
                label={seatClass}
                className="bg-airline-gold text-airline-navy font-semibold"
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Grid container spacing={4}>
        {/* Filters */}
        <Grid item xs={12} md={3}>
          <Paper className="p-4 rounded-2xl sticky top-24">
            <Typography variant="h6" className="font-bold mb-4">Bộ lọc</Typography>

            <Typography variant="subtitle2" className="font-semibold mb-2">
              <AttachMoney className="text-airline-blue" /> Giá vé
            </Typography>
            <Box className="px-2">
              <Slider
                value={priceRange}
                onChange={(_, newValue) => setPriceRange(newValue)}
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => formatPrice(value)}
                max={maxPrice}
                className="text-airline-blue"
              />
              <Box className="flex justify-between text-sm text-gray-500">
                <span>{formatPrice(priceRange[0])}</span>
                <span>{formatPrice(priceRange[1])}</span>
              </Box>
            </Box>

            <Box className="mt-4">
              <FormControlLabel
                control={
                  <Switch
                    checked={showOnlyAvailable}
                    onChange={(e) => setShowOnlyAvailable(e.target.checked)}
                    className="text-airline-blue"
                  />
                }
                label="Còn ghế trống"
              />
            </Box>

            <Box className="mt-4">
              <Typography variant="subtitle2" className="font-semibold mb-2">
                Sắp xếp theo
              </Typography>
              <Box className="flex flex-col gap-2">
                <Button
                  variant={sortBy === 'price' ? 'contained' : 'outlined'}
                  size="small"
                  onClick={() => setSortBy('price')}
                  className={sortBy === 'price' ? 'bg-airline-blue' : 'border-airline-blue text-airline-blue'}
                >
                  Giá thấp nhất
                </Button>
                <Button
                  variant={sortBy === 'time' ? 'contained' : 'outlined'}
                  size="small"
                  onClick={() => setSortBy('time')}
                  className={sortBy === 'time' ? 'bg-airline-blue' : 'border-airline-blue text-airline-blue'}
                >
                  Giờ khởi hành
                </Button>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Results */}
        <Grid item xs={12} md={9}>
          <Box className="flex items-center justify-between mb-4">
            <Typography variant="h5" className="font-bold">
              {filteredFlights.length} chuyến bay
            </Typography>
            <Typography variant="body2" className="text-gray-500">
              {flights.length} chuyến tìm thấy
            </Typography>
          </Box>

          {filteredFlights.length === 0 ? (
            <Paper className="p-12 text-center rounded-2xl">
              <Typography variant="h6" className="text-gray-500">
                Không tìm thấy chuyến bay phù hợp
              </Typography>
              <Button
                variant="outlined"
                onClick={() => {
                  setPriceRange([0, maxPrice]);
                  setShowOnlyAvailable(false);
                }}
                className="mt-4"
              >
                Xóa bộ lọc
              </Button>
            </Paper>
          ) : (
            <Box className="space-y-4">
              {filteredFlights.map((flight) => (
                <FlightCard
                  key={flight.flight_id}
                  flight={flight}
                  onBook={handleBook}
                />
              ))}
            </Box>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default SearchFlights;