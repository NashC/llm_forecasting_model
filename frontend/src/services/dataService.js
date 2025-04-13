import api from './api';

export const getDataSources = async (type = null, page = 1, limit = 10) => {
  const params = { skip: (page - 1) * limit, limit };
  if (type) {
    params.source_type = type;
  }
  
  const response = await api.get('/data-sources', { params });
  return response.data;
};

export const getDataSourceById = async (id) => {
  const response = await api.get(`/data-sources/${id}`);
  return response.data;
};

export const createDataSource = async (dataSourceData) => {
  const response = await api.post('/data-sources', dataSourceData);
  return response.data;
};

export const updateDataSource = async (id, dataSourceData) => {
  const response = await api.put(`/data-sources/${id}`, dataSourceData);
  return response.data;
};

export const deleteDataSource = async (id) => {
  const response = await api.delete(`/data-sources/${id}`);
  return response.data;
};

export const uploadFileData = async (file, name, sourceType, description = '') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('source_type', sourceType);
  
  if (description) {
    formData.append('description', description);
  }
  
  const response = await api.post('/data-sources/upload/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const importDataFromSource = async (sourceId) => {
  const response = await api.post(`/data-sources/${sourceId}/import`);
  return response.data;
}; 