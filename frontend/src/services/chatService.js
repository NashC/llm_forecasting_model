import api from './api';

export const sendMessage = async (message, conversationId = null, context = null) => {
  const data = { message };
  
  if (conversationId) {
    data.conversation_id = conversationId;
  }
  
  if (context) {
    data.context = context;
  }
  
  const response = await api.post('/chat/message', data);
  return response.data;
};

export const generateForecast = async (message, modelType, historicalData = null, assumptions = null) => {
  const data = {
    message,
    model_type: modelType,
  };
  
  if (historicalData) {
    data.historical_data = historicalData;
  }
  
  if (assumptions) {
    data.assumptions = assumptions;
  }
  
  const response = await api.post('/chat/generate-forecast', data);
  return response.data;
}; 