import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Typography, Button, Container, Paper } from '@mui/material';
import { Error } from '@mui/icons-material';

const NotFoundPage = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          textAlign: 'center',
          p: 4,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 5,
            borderRadius: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Error sx={{ fontSize: 80, color: 'error.main', mb: 2 }} />
          <Typography variant="h3" component="h1" gutterBottom>
            404: Page Not Found
          </Typography>
          <Typography variant="body1" paragraph>
            The page you're looking for doesn't exist or has been moved.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            component={RouterLink}
            to="/"
            sx={{ mt: 2 }}
          >
            Return to Dashboard
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default NotFoundPage; 