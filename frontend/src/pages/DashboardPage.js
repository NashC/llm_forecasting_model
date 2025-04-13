import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Divider,
  Chip,
  Link,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add,
  TrendingUp,
  BarChart,
  DataObject,
  Chat,
  ArrowForward,
  MoreVert,
} from '@mui/icons-material';
import { getModels } from '../services/modelService';
import Loading from '../components/common/Loading';
import ErrorAlert from '../components/common/ErrorAlert';
import { useAuth } from '../hooks/useAuth';

const DashboardPage = () => {
  const { currentUser } = useAuth();
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setLoading(true);
        const data = await getModels(null, 1, 4); // Get first 4 models
        setModels(data);
      } catch (err) {
        console.error('Error fetching models:', err);
        setError('Failed to load models. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  return (
    <Box>
      {/* Welcome header */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 4,
          borderRadius: 2,
          bgcolor: 'primary.light',
          color: 'primary.contrastText',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              Welcome back, {currentUser?.full_name || currentUser?.username || 'User'}!
            </Typography>
            <Typography variant="body1">
              Ready to create financial models with the power of AI? Get started by creating a new model or using the assistant.
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<Add />}
              component={RouterLink}
              to="/models/create"
            >
              New Model
            </Button>
            <Button
              variant="outlined"
              sx={{ bgcolor: 'white', color: 'primary.main' }}
              startIcon={<Chat />}
              component={RouterLink}
              to="/assistant"
            >
              Ask Assistant
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* Quick actions */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{ p: 3, textAlign: 'center', height: '100%', borderRadius: 2 }}
            component={RouterLink}
            to="/models/create"
            style={{ textDecoration: 'none', display: 'block' }}
          >
            <TrendingUp sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
            <Typography variant="h6" gutterBottom>
              Create Forecast
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Generate a new financial forecast with AI assistance
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{ p: 3, textAlign: 'center', height: '100%', borderRadius: 2 }}
            component={RouterLink}
            to="/models"
            style={{ textDecoration: 'none', display: 'block' }}
          >
            <BarChart sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
            <Typography variant="h6" gutterBottom>
              View Models
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Browse and manage your existing financial models
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{ p: 3, textAlign: 'center', height: '100%', borderRadius: 2 }}
            component={RouterLink}
            to="/code-editor"
            style={{ textDecoration: 'none', display: 'block' }}
          >
            <DataObject sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
            <Typography variant="h6" gutterBottom>
              Code Editor
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Edit and customize model code directly
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{ p: 3, textAlign: 'center', height: '100%', borderRadius: 2 }}
            component={RouterLink}
            to="/data-sources"
            style={{ textDecoration: 'none', display: 'block' }}
          >
            <DataObject sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
            <Typography variant="h6" gutterBottom>
              Data Sources
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage and import data from various sources
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent models */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5" component="h2">
            Recent Models
          </Typography>
          <Button
            component={RouterLink}
            to="/models"
            endIcon={<ArrowForward />}
            color="primary"
          >
            View All
          </Button>
        </Box>
        
        {loading ? (
          <Loading message="Loading recent models..." />
        ) : error ? (
          <ErrorAlert error={error} />
        ) : models.length === 0 ? (
          <Paper sx={{ p: 3, textAlign: 'center', borderRadius: 2 }}>
            <Typography variant="body1" color="text.secondary" paragraph>
              You don't have any models yet.
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              component={RouterLink}
              to="/models/create"
            >
              Create Your First Model
            </Button>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {models.map((model) => (
              <Grid item xs={12} sm={6} md={3} key={model.id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', borderRadius: 2 }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="h6" component="h3" noWrap>
                        {model.name}
                      </Typography>
                      <Tooltip title="More options">
                        <IconButton size="small">
                          <MoreVert fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      {model.description ? model.description.substring(0, 60) + (model.description.length > 60 ? '...' : '') : 'No description'}
                    </Typography>
                    <Chip
                      label={model.model_type}
                      size="small"
                      color={
                        model.model_type === 'revenue' ? 'success' :
                        model.model_type === 'expense' ? 'error' :
                        model.model_type === 'cash_flow' ? 'info' :
                        'default'
                      }
                      sx={{ mr: 1 }}
                    />
                  </CardContent>
                  <Divider />
                  <CardActions>
                    <Button
                      size="small"
                      component={RouterLink}
                      to={`/models/${model.id}`}
                    >
                      View
                    </Button>
                    <Button
                      size="small"
                      component={RouterLink}
                      to={`/models/${model.id}/run`}
                    >
                      Run
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Box>
  );
};

export default DashboardPage; 