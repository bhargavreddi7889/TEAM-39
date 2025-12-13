import axios from 'axios';

// API Base URL - proxied through Vite to backend at localhost:8000
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API (mock - no backend auth yet)
export const authAPI = {
  login: (credentials) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const { username, password, role } = credentials;
        
        // Demo credentials
        if (
          (role === 'student' && username === 'student' && password === 'student123') ||
          (role === 'admin' && username === 'admin' && password === 'admin123')
        ) {
          resolve({
            data: {
              user: { username, role },
              token: `${role}_token_${Date.now()}`,
            },
          });
        } else {
          reject(new Error('Invalid credentials'));
        }
      }, 500);
    });
  },
};

// Query API (Student endpoints)
export const queryAPI = {
  askQuestion: (question) => api.post('/query/', { query: question }),
};

// Admin API (matches backend routes)
export const adminAPI = {
  // GET /admin/stats - Knowledge base statistics
  getStats: () => api.get('/admin/stats'),
  
  // POST /admin/ingest - Direct document ingestion
  ingestDocuments: (documents) => 
    api.post('/admin/ingest', { documents }),
  
  // POST /admin/files - Upload a file
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/admin/files', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // GET /admin/files - List all files
  listFiles: () => api.get('/admin/files'),
  
  // GET /admin/files/{filename} - Download a file
  downloadFile: (filename) => api.get(`/admin/files/${filename}`),
  
  // DELETE /admin/files/{filename} - Delete a file
  deleteFile: (filename) => api.delete(`/admin/files/${filename}`),
  
  // POST /admin/reindex - Re-index all files
  reindexAll: (clearExisting = true) => 
    api.post(`/admin/reindex?clear_existing=${clearExisting}`),
};

// Health API
export const healthAPI = {
  check: () => api.get('/'),  // Backend health check is at root
};

export default api;

