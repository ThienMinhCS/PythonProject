// src/components/common/Header.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Menu,
  MenuItem,
  Avatar,
  IconButton,
} from '@mui/material';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleClose();
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'white' }}>
          ✈️ Airline Booking
        </Typography>

        <Button color="inherit" component={Link} to="/search">
          Tìm chuyến bay
        </Button>

        {user ? (
          <Box>
            <IconButton onClick={handleMenu} color="inherit">
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {user.full_name?.charAt(0)}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleClose} component={Link} to="/profile">
                Hồ sơ
              </MenuItem>
              <MenuItem onClick={handleClose} component={Link} to="/bookings">
                Lịch sử đặt vé
              </MenuItem>
              <MenuItem onClick={handleLogout}>Đăng xuất</MenuItem>
            </Menu>
          </Box>
        ) : (
          <Box>
            <Button color="inherit" component={Link} to="/login">
              Đăng nhập
            </Button>
            <Button color="inherit" component={Link} to="/register">
              Đăng ký
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header;  // 👈 PHẢI CÓ DÒNG NÀY