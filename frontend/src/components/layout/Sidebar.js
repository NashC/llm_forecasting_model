import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Toolbar,
  Typography,
} from '@mui/material';
import {
  Dashboard,
  BarChart,
  Chat,
  DataObject,
  Storage,
  Settings,
  Help,
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
  { text: 'Forecasting Models', icon: <BarChart />, path: '/models' },
  { text: 'AI Assistant', icon: <Chat />, path: '/assistant' },
  { text: 'Data Sources', icon: <Storage />, path: '/data-sources' },
  { text: 'Code Editor', icon: <DataObject />, path: '/code-editor' },
];

const secondaryMenuItems = [
  { text: 'Settings', icon: <Settings />, path: '/settings' },
  { text: 'Help', icon: <Help />, path: '/help' },
];

const Sidebar = ({ mobileOpen, onDrawerToggle, window }) => {
  const { currentUser } = useAuth();
  const location = useLocation();
  
  const container = window !== undefined ? () => window().document.body : undefined;
  
  const drawer = (
    <div>
      <Toolbar />
      <Box sx={{ p: 2 }}>
        <Typography variant="subtitle1" fontWeight="bold">
          Main
        </Typography>
      </Box>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={RouterLink}
              to={item.path}
              selected={location.pathname === item.path}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider sx={{ my: 2 }} />
      <Box sx={{ p: 2 }}>
        <Typography variant="subtitle1" fontWeight="bold">
          System
        </Typography>
      </Box>
      <List>
        {secondaryMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={RouterLink}
              to={item.path}
              selected={location.pathname === item.path}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  // If user is not logged in, don't render the sidebar
  if (!currentUser) {
    return null;
  }

  return (
    <Box
      component="nav"
      sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      aria-label="navigation sidebar"
    >
      {/* Mobile drawer */}
      <Drawer
        container={container}
        variant="temporary"
        open={mobileOpen}
        onClose={onDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawer}
      </Drawer>
      
      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', md: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
};

export default Sidebar; 