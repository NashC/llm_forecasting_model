import React, { createContext, useState, useEffect } from 'react';
import { loginUser, registerUser, getCurrentUser, refreshToken } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkLoggedIn = async () => {
      setLoading(true);
      try {
        // Check if user is already logged in
        const token = localStorage.getItem('token');
        const refreshTokenValue = localStorage.getItem('refreshToken');
        
        if (token) {
          try {
            // Try to get current user with existing token
            const userData = await getCurrentUser();
            setCurrentUser(userData);
          } catch (err) {
            // If token is expired, try to refresh it
            if (refreshTokenValue) {
              try {
                const refreshResponse = await refreshToken(refreshTokenValue);
                localStorage.setItem('token', refreshResponse.access_token);
                localStorage.setItem('refreshToken', refreshResponse.refresh_token);
                
                // Now try again with the new token
                const userData = await getCurrentUser();
                setCurrentUser(userData);
              } catch (refreshErr) {
                // If refresh fails, log out user
                logout();
              }
            } else {
              // No refresh token available, log out user
              logout();
            }
          }
        }
      } catch (err) {
        console.error('Error checking authentication status:', err);
        setError('Authentication error. Please log in again.');
        logout();
      } finally {
        setLoading(false);
      }
    };

    checkLoggedIn();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await loginUser(email, password);
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('refreshToken', response.refresh_token);
      
      const userData = await getCurrentUser();
      setCurrentUser(userData);
      return userData;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await registerUser(userData);
      return response;
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    loading,
    error,
    login,
    register,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 