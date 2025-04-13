import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Divider,
  Avatar,
  Grid,
  IconButton,
  CircularProgress,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { Send, SmartToy, Person, Code, SaveAlt } from '@mui/icons-material';
import { sendMessage, generateForecast } from '../services/chatService';
import { createModel } from '../services/modelService';
import { useAuth } from '../hooks/useAuth';
import ErrorAlert from '../components/common/ErrorAlert';

const AssistantPage = () => {
  const { currentUser } = useAuth();
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages when conversation updates
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation]);

  const handleMessageSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message to conversation
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };
    setConversation((prev) => [...prev, userMessage]);
    setMessage('');
    setLoading(true);
    setError(null);

    try {
      // Send message to API
      const response = await sendMessage(message, conversationId);
      
      // If this is the first message, save the conversation ID
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }
      
      // Add assistant response to conversation
      const assistantMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      };
      setConversation((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateModel = async () => {
    if (conversation.length < 2) {
      setError('Please have a conversation with the assistant first.');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      // Extract the last user message as the prompt
      const lastUserMessage = [...conversation]
        .reverse()
        .find((msg) => msg.role === 'user')?.content;
        
      if (!lastUserMessage) {
        throw new Error('No user message found.');
      }
      
      // Generate forecast code
      const response = await generateForecast(
        lastUserMessage,
        'revenue', // Default model type
      );
      
      // Create a new model with the generated code
      const modelData = {
        name: `Model from conversation ${new Date().toLocaleDateString()}`,
        description: lastUserMessage,
        model_type: response.model_type,
        code: response.code,
        parameters: response.parameters,
        is_public: false,
      };
      
      const createdModel = await createModel(modelData);
      
      // Add system message about successful creation
      const systemMessage = {
        role: 'system',
        content: `Model created successfully! [View Model](#/models/${createdModel.id})`,
        timestamp: new Date().toISOString(),
      };
      setConversation((prev) => [...prev, systemMessage]);
      
    } catch (err) {
      console.error('Error generating model:', err);
      setError('Failed to generate model. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Format message content with code blocks
  const formatMessageContent = (content) => {
    if (!content.includes('```')) return content;
    
    const parts = content.split(/```([\s\S]*?)```/);
    return parts.map((part, index) => {
      // Even indices are regular text, odd indices are code blocks
      if (index % 2 === 0) {
        return <Typography key={index} variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{part}</Typography>;
      } else {
        return (
          <Paper key={index} sx={{ p: 2, my: 2, bgcolor: 'grey.900', borderRadius: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography variant="caption" color="grey.500">Code</Typography>
              <IconButton size="small" color="inherit">
                <SaveAlt fontSize="small" />
              </IconButton>
            </Box>
            <Box component="pre" sx={{ m: 0, overflow: 'auto', fontSize: '0.875rem', color: 'grey.300' }}>
              <code>{part}</code>
            </Box>
          </Paper>
        );
      }
    });
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        AI Financial Assistant
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Ask questions about financial modeling, request forecasts, or get help analyzing data.
      </Typography>
      
      {error && <ErrorAlert error={error} />}
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          {/* Chat interface */}
          <Paper
            sx={{
              p: 2,
              height: '65vh',
              display: 'flex',
              flexDirection: 'column',
              borderRadius: 2,
            }}
          >
            {/* Messages area */}
            <Box
              sx={{
                flexGrow: 1,
                overflow: 'auto',
                p: 2,
              }}
            >
              {conversation.length === 0 ? (
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    textAlign: 'center',
                  }}
                >
                  <SmartToy sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    AI Financial Assistant
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ maxWidth: '70%' }}>
                    Ask me about creating financial models, analyzing data, or generating forecasts. I can help you build and understand financial projections.
                  </Typography>
                </Box>
              ) : (
                conversation.map((msg, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      mb: 2,
                      flexDirection: msg.role === 'user' ? 'row-reverse' : 'row',
                    }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: msg.role === 'user' ? 'secondary.main' : 'primary.main',
                        width: 36,
                        height: 36,
                      }}
                    >
                      {msg.role === 'user' ? <Person /> : msg.role === 'system' ? <Code /> : <SmartToy />}
                    </Avatar>
                    <Paper
                      sx={{
                        p: 2,
                        ml: msg.role === 'user' ? 0 : 1,
                        mr: msg.role === 'user' ? 1 : 0,
                        maxWidth: '80%',
                        bgcolor: msg.role === 'user' ? 'secondary.light' : msg.role === 'system' ? 'grey.200' : 'background.paper',
                        borderRadius: 2,
                      }}
                    >
                      {formatMessageContent(msg.content)}
                    </Paper>
                  </Box>
                ))
              )}
              <div ref={messagesEndRef} />
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            {/* Input area */}
            <Box component="form" onSubmit={handleMessageSubmit}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  placeholder="Ask about financial forecasting..."
                  variant="outlined"
                  size="medium"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  disabled={loading}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  endIcon={loading ? <CircularProgress size={16} color="inherit" /> : <Send />}
                  disabled={!message.trim() || loading}
                >
                  {loading ? 'Sending' : 'Send'}
                </Button>
              </Box>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          {/* Options and tools panel */}
          <Card sx={{ mb: 3, borderRadius: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tools
              </Typography>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<Code />}
                onClick={handleGenerateModel}
                disabled={loading || conversation.length < 2}
                sx={{ mb: 2 }}
              >
                Generate Model from Conversation
              </Button>
              <Typography variant="body2" color="text.secondary">
                Convert this conversation into a functional financial model.
              </Typography>
            </CardContent>
          </Card>
          
          <Card sx={{ borderRadius: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Example Prompts
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Chip
                  label="Create a 3-year revenue forecast with 5% monthly growth"
                  clickable
                  onClick={() => setMessage("Create a 3-year revenue forecast with 5% monthly growth")}
                />
                <Chip
                  label="Help me model cash flow with 45-day collection period"
                  clickable
                  onClick={() => setMessage("Help me model cash flow with 45-day collection period")}
                />
                <Chip
                  label="Create an expense model with fixed and variable costs"
                  clickable
                  onClick={() => setMessage("Create an expense model with fixed and variable costs")}
                />
                <Chip
                  label="How do I calculate break-even point?"
                  clickable
                  onClick={() => setMessage("How do I calculate break-even point?")}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AssistantPage; 