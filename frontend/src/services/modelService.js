import api from './api';

export const getModels = async (type = null, page = 1, limit = 10) => {
  let url = '/models';
  const params = { skip: (page - 1) * limit, limit };
  if (type) {
    params.model_type = type;
  }
  
  const response = await api.get(url, { params });
  return response.data;
};

export const getModelById = async (id) => {
  const response = await api.get(`/models/${id}`);
  return response.data;
};

export const createModel = async (modelData) => {
  const response = await api.post('/models', modelData);
  return response.data;
};

export const updateModel = async (id, modelData) => {
  const response = await api.put(`/models/${id}`, modelData);
  return response.data;
};

export const deleteModel = async (id) => {
  const response = await api.delete(`/models/${id}`);
  return response.data;
};

export const runModel = async (id, parameters = null) => {
  const response = await api.post(`/models/${id}/run`, { parameters });
  return response.data;
};

export const generateModel = async (modelType, prompt, parameters = null) => {
  const params = { model_type: modelType };
  const data = { message: prompt };
  
  if (parameters) {
    data.parameters = parameters;
  }
  
  const response = await api.post('/models/generate', data, { params });
  return response.data;
};

export const getModelVersions = async (modelId) => {
  const response = await api.get(`/models/${modelId}/versions`);
  return response.data;
};

export const getModelVersion = async (modelId, versionNumber) => {
  const response = await api.get(`/models/${modelId}/versions/${versionNumber}`);
  return response.data;
}; 