import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, Toolbar, Container } from '@mui/material';
import AppNavbar from './AppNavbar';
import Sidebar from './Sidebar';
import { useAuth } from '../../hooks/useAuth';

const drawerWidth = 240;

const AppLayout = () => {
  const { currentUser } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppNavbar onDrawerToggle={handleDrawerToggle} />
      
      <Sidebar
        mobileOpen={mobileOpen}
        onDrawerToggle={handleDrawerToggle}
      />
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { md: `calc(100% - ${currentUser ? drawerWidth : 0}px)` },
          bgcolor: 'background.default',
        }}
      >
        <Toolbar /> {/* Ensures content is below the AppBar */}
        <Container maxWidth="xl" sx={{ py: 3 }}>
          <Outlet />
        </Container>
      </Box>
    </Box>
  );
};

export default AppLayout; 