import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';

import AppLayout from './components/layout/AppLayout';
import Loading from './components/common/Loading';
import { useAuth } from './hooks/useAuth';

// Lazy load pages for better performance
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ModelsPage = lazy(() => import('./pages/ModelsPage'));
const ModelDetailPage = lazy(() => import('./pages/ModelDetailPage'));
const CreateModelPage = lazy(() => import('./pages/CreateModelPage'));
const AssistantPage = lazy(() => import('./pages/AssistantPage'));
const DataSourcesPage = lazy(() => import('./pages/DataSourcesPage'));
const DataSourceDetailPage = lazy(() => import('./pages/DataSourceDetailPage'));
const CodeEditorPage = lazy(() => import('./pages/CodeEditorPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'));

// Route guard for protected routes
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  
  if (loading) {
    return <Loading message="Authenticating..." />;
  }
  
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Suspense
      fallback={
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
        >
          <CircularProgress />
        </Box>
      }
    >
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="models" element={<ModelsPage />} />
          <Route path="models/:id" element={<ModelDetailPage />} />
          <Route path="models/create" element={<CreateModelPage />} />
          <Route path="assistant" element={<AssistantPage />} />
          <Route path="data-sources" element={<DataSourcesPage />} />
          <Route path="data-sources/:id" element={<DataSourceDetailPage />} />
          <Route path="code-editor" element={<CodeEditorPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>
        
        {/* Catch-all route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}

export default App; 