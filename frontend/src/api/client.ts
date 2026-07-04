import axios from 'axios';

// Points to FastAPI backend via Vite proxy (/api → http://localhost:8000)
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

export default apiClient;
