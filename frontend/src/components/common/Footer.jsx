import React from 'react';
import { Box, Container, Grid, Typography, Link, Divider, IconButton } from '@mui/material';
import {
  FlightTakeoff,
  Phone,
  Email,
  LocationOn,
  Facebook,
  Instagram,
  YouTube,
  Twitter,
  Language,
} from '@mui/icons-material';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: '#0A1E3C',
        color: 'white',
        borderTop: '3px solid #F1C40F',
        mt: 'auto',
      }}
    >
      {/* Main Footer */}
      <Container maxWidth="xl" className="py-12">
        <Grid container spacing={4}>
          {/* Brand */}
          <Grid item xs={12} md={4}>
            <Box className="flex items-center gap-2 mb-4">
              <FlightTakeoff sx={{ color: '#F1C40F', fontSize: 35 }} />
              <Typography variant="h5" className="font-bold">
                Airline<span style={{ color: '#F1C40F' }}>Viet</span>
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', lineHeight: 1.8 }}>
              Hệ thống đặt vé máy bay trực tuyến hàng đầu Việt Nam.
              Cam kết mang đến trải nghiệm bay tốt nhất với giá cả hợp lý
              và dịch vụ chuyên nghiệp.
            </Typography>
            <Box className="flex gap-2 mt-4">
              <IconButton
                sx={{
                  color: 'rgba(255,255,255,0.5)',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                <Facebook />
              </IconButton>
              <IconButton
                sx={{
                  color: 'rgba(255,255,255,0.5)',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                <Instagram />
              </IconButton>
              <IconButton
                sx={{
                  color: 'rgba(255,255,255,0.5)',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                <YouTube />
              </IconButton>
              <IconButton
                sx={{
                  color: 'rgba(255,255,255,0.5)',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                <Twitter />
              </IconButton>
            </Box>
          </Grid>

          {/* Quick Links */}
          <Grid item xs={6} md={2}>
            <Typography variant="subtitle1" className="font-bold mb-4" sx={{ color: '#F1C40F' }}>
              Về chúng tôi
            </Typography>
            <Box className="space-y-2">
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Giới thiệu
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Tuyển dụng
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Tin tức
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Khuyến mãi
              </Link>
            </Box>
          </Grid>

          {/* Support */}
          <Grid item xs={6} md={2}>
            <Typography variant="subtitle1" className="font-bold mb-4" sx={{ color: '#F1C40F' }}>
              Hỗ trợ
            </Typography>
            <Box className="space-y-2">
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Trung tâm hỗ trợ
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                FAQ
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Điều khoản sử dụng
              </Link>
              <Link
                href="#"
                sx={{
                  display: 'block',
                  color: 'rgba(255,255,255,0.7)',
                  textDecoration: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { color: '#F1C40F' },
                  transition: 'color 0.3s',
                }}
              >
                Chính sách bảo mật
              </Link>
            </Box>
          </Grid>

          {/* Contact */}
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" className="font-bold mb-4" sx={{ color: '#F1C40F' }}>
              Liên hệ
            </Typography>
            <Box className="space-y-3">
              <Box className="flex items-start gap-3">
                <LocationOn sx={{ color: '#F1C40F', mt: 0.5 }} />
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  123 Đường Lê Lợi, Quận 1, TP. Hồ Chí Minh
                </Typography>
              </Box>
              <Box className="flex items-center gap-3">
                <Phone sx={{ color: '#F1C40F' }} />
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  <strong>Hotline:</strong> 1900 1234
                </Typography>
              </Box>
              <Box className="flex items-center gap-3">
                <Email sx={{ color: '#F1C40F' }} />
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  <strong>Email:</strong> support@airlineviet.com
                </Typography>
              </Box>
              <Box className="flex items-center gap-3">
                <Language sx={{ color: '#F1C40F' }} />
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  <strong>Website:</strong> www.airlineviet.com
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* Divider */}
        <Divider sx={{ backgroundColor: 'rgba(255,255,255,0.1)', my: 4 }} />

        {/* Bottom Bar */}
        <Box className="flex flex-col md:flex-row justify-between items-center gap-4">
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.4)' }}>
            © {currentYear} AirlineViet. All rights reserved.
          </Typography>
          <Box className="flex gap-6">
            <Link
              href="#"
              sx={{
                color: 'rgba(255,255,255,0.4)',
                textDecoration: 'none',
                fontSize: '0.85rem',
                '&:hover': { color: '#F1C40F' },
                transition: 'color 0.3s',
              }}
            >
              Điều khoản
            </Link>
            <Link
              href="#"
              sx={{
                color: 'rgba(255,255,255,0.4)',
                textDecoration: 'none',
                fontSize: '0.85rem',
                '&:hover': { color: '#F1C40F' },
                transition: 'color 0.3s',
              }}
            >
              Bảo mật
            </Link>
            <Link
              href="#"
              sx={{
                color: 'rgba(255,255,255,0.4)',
                textDecoration: 'none',
                fontSize: '0.85rem',
                '&:hover': { color: '#F1C40F' },
                transition: 'color 0.3s',
              }}
            >
              Cookies
            </Link>
          </Box>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.8rem' }}>
            Made with ❤️ in Vietnam
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;