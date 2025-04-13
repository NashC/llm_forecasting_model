import React from 'react';
import { Alert, AlertTitle, Box } from '@mui/material';

const ErrorAlert = ({ error, severity = 'error', title, onClose }) => {
  if (!error) return null;

  let errorMessage = '';
  if (typeof error === 'string') {
    errorMessage = error;
  } else if (error.message) {
    errorMessage = error.message;
  } else if (error.response?.data?.detail) {
    errorMessage = error.response.data.detail;
  } else {
    errorMessage = 'An unexpected error occurred.';
  }

  return (
    <Box sx={{ my: 2 }}>
      <Alert severity={severity} onClose={onClose}>
        {title && <AlertTitle>{title}</AlertTitle>}
        {errorMessage}
      </Alert>
    </Box>
  );
};

export default ErrorAlert; 