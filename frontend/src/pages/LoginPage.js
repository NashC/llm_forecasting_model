import React, { useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { Box, Typography, Container, Paper } from '@mui/material';
import LoginForm from '../components/auth/LoginForm';
import { useAuth } from '../hooks/useAuth';

const LoginPage = () => {
  const { currentUser } = useAuth();

  // If user is already logged in, redirect to dashboard
  if (currentUser) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <Container component="main" maxWidth="lg">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          py: 4,
        }}
      >
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            LLM Financial Forecasting
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Sign in to access your AI-powered financial models
          </Typography>
        </Box>
        
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            flexDirection: { xs: 'column', md: 'row' },
            gap: 4,
          }}
        >
          <Box
            sx={{
              flex: 1,
              display: { xs: 'none', md: 'flex' },
              flexDirection: 'column',
              justifyContent: 'center',
            }}
          >
            <Paper
              elevation={0}
              sx={{
                p: 4,
                bgcolor: 'primary.main',
                color: 'white',
                borderRadius: 2,
              }}
            >
              <Typography variant="h5" gutterBottom>
                Transform Your Financial Modeling
              </Typography>
              <Typography variant="body1" paragraph>
                Our AI-driven platform helps you create, refine, and share sophisticated
                financial models through natural language conversations.
              </Typography>
              <Typography variant="body1">
                Save time, reduce errors, and gain valuable insights with automated
                forecasting tailored to your business needs.
              </Typography>
            </Paper>
          </Box>
          
          <Box sx={{ flex: 1 }}>
            <LoginForm />
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage; 