import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
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
  Tooltip,
  Badge,
  Container,
  Divider,
} from '@mui/material';
import {
  Home,
  FlightTakeoff,
  Bookmark,
  Person,
  AdminPanelSettings,
  Notifications,
  Logout,
  Dashboard,
  Menu as MenuIcon,
} from '@mui/icons-material';

const Header = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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

  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', label: 'Trang chủ', icon: <Home /> },
    { path: '/search', label: 'Tìm chuyến bay', icon: <FlightTakeoff /> },
    ...(isAuthenticated ? [{ path: '/bookings', label: 'Đặt vé của tôi', icon: <Bookmark /> }] : []),
    ...(isAdmin ? [{ path: '/admin', label: 'Admin', icon: <AdminPanelSettings /> }] : []),
  ];

  return (
    <AppBar 
      position="sticky" 
      elevation={0}
      sx={{
        backgroundColor: '#0A1E3C',
        borderBottom: '3px solid #F1C40F',
      }}
    >
      <Container maxWidth="xl">
        <Toolbar className="px-0" sx={{ minHeight: { xs: 64, md: 72 } }}>
          {/* Logo */}
          <Typography
            variant="h6"
            component={Link}
            to="/"
            className="flex items-center gap-2 font-bold no-underline"
            sx={{
              color: 'white',
              fontSize: { xs: '1.1rem', md: '1.5rem' },
              '&:hover': { color: '#F1C40F' },
              transition: 'color 0.3s',
            }}
          >
            <FlightTakeoff sx={{ color: '#F1C40F', fontSize: { xs: 28, md: 35 } }} />
            <span className="hidden sm:inline">Airline</span>
            <span style={{ color: '#F1C40F' }}>Viet</span>
          </Typography>

          {/* Desktop Navigation */}
          <Box className="hidden md:flex items-center gap-1 ml-8">
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={Link}
                to={item.path}
                startIcon={item.icon}
                sx={{
                  color: isActive(item.path) ? '#F1C40F' : 'white',
                  backgroundColor: isActive(item.path) ? 'rgba(241, 196, 15, 0.1)' : 'transparent',
                  borderRadius: '12px',
                  px: 3,
                  py: 1.2,
                  fontWeight: isActive(item.path) ? 700 : 500,
                  fontSize: '0.95rem',
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: 'rgba(241, 196, 15, 0.15)',
                    color: '#F1C40F',
                  },
                  transition: 'all 0.3s',
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>

          {/* Right Section */}
          <Box className="flex items-center gap-2 ml-auto">
            {isAuthenticated ? (
              <>
                {/* Notification */}
                <Tooltip title="Thông báo">
                  <IconButton 
                    color="inherit" 
                    sx={{ 
                      color: 'white',
                      '&:hover': { backgroundColor: 'rgba(255,255,255,0.1)' },
                    }}
                  >
                    <Badge badgeContent={3} color="error">
                      <Notifications />
                    </Badge>
                  </IconButton>
                </Tooltip>

                {/* User Menu */}
                <Tooltip title={user?.full_name || 'User'}>
                  <IconButton
                    onClick={handleMenu}
                    sx={{
                      p: 0.5,
                      border: '2px solid #F1C40F',
                      '&:hover': { borderColor: 'white' },
                      transition: 'border-color 0.3s',
                    }}
                  >
                    <Avatar 
                      sx={{ 
                        width: 40, 
                        height: 40, 
                        bgcolor: '#F1C40F',
                        color: '#0A1E3C',
                        fontWeight: 'bold',
                        fontSize: '1.1rem',
                      }}
                    >
                      {user?.full_name?.charAt(0).toUpperCase() || 'U'}
                    </Avatar>
                  </IconButton>
                </Tooltip>

                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                  PaperProps={{
                    sx: {
                      mt: 1.5,
                      borderRadius: '16px',
                      minWidth: 220,
                      boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
                      '& .MuiMenuItem-root': {
                        py: 1.5,
                        px: 2.5,
                        gap: 2,
                        fontSize: '0.95rem',
                      },
                    },
                  }}
                >
                  <Box sx={{ px: 2.5, py: 1.5, bgcolor: '#f5f5f5' }}>
                    <Typography variant="subtitle2" className="font-bold">
                      {user?.full_name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {user?.email}
                    </Typography>
                  </Box>
                  <Divider />
                  <MenuItem onClick={handleClose} component={Link} to="/profile">
                    <Person fontSize="small" /> Hồ sơ cá nhân
                  </MenuItem>
                  <MenuItem onClick={handleClose} component={Link} to="/bookings">
                    <Bookmark fontSize="small" /> Lịch sử đặt vé
                  </MenuItem>
                  {isAdmin && (
                    <MenuItem onClick={handleClose} component={Link} to="/admin">
                      <Dashboard fontSize="small" sx={{ color: '#F1C40F' }} /> 
                      <span style={{ color: '#F1C40F' }}>Admin Panel</span>
                    </MenuItem>
                  )}
                  <Divider />
                  <MenuItem onClick={handleLogout} sx={{ color: '#E74C3C' }}>
                    <Logout fontSize="small" /> Đăng xuất
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Box className="flex gap-2">
                <Button
                  component={Link}
                  to="/login"
                  sx={{
                    color: 'white',
                    border: '1px solid rgba(255,255,255,0.3)',
                    borderRadius: '12px',
                    px: 3,
                    py: 1,
                    textTransform: 'none',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255,255,255,0.05)',
                    },
                  }}
                >
                  Đăng nhập
                </Button>
                <Button
                  component={Link}
                  to="/register"
                  sx={{
                    backgroundColor: '#F1C40F',
                    color: '#0A1E3C',
                    borderRadius: '12px',
                    px: 3,
                    py: 1,
                    fontWeight: 700,
                    textTransform: 'none',
                    '&:hover': {
                      backgroundColor: '#f39c12',
                    },
                  }}
                >
                  Đăng ký
                </Button>
              </Box>
            )}

            {/* Mobile Menu Button */}
            <IconButton
              color="inherit"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              sx={{ color: 'white' }}
            >
              <MenuIcon />
            </IconButton>
          </Box>
        </Toolbar>
      </Container>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <Box
          sx={{
            backgroundColor: '#0A1E3C',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            py: 2,
          }}
          className="md:hidden"
        >
          <Container>
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={Link}
                to={item.path}
                fullWidth
                startIcon={item.icon}
                onClick={() => setMobileMenuOpen(false)}
                sx={{
                  color: isActive(item.path) ? '#F1C40F' : 'white',
                  justifyContent: 'flex-start',
                  py: 1.5,
                  px: 2,
                  borderRadius: '12px',
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: 'rgba(241, 196, 15, 0.1)',
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Container>
        </Box>
      )}
    </AppBar>
  );
};

export default Header;