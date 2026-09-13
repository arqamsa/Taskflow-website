import axios from 'axios'

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('taskflow_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authApi = {
  login: (payload) => api.post('/auth/login', payload),
  register: (payload) => api.post('/auth/register', payload),
  me: () => api.get('/auth/me'),
}

export const projectApi = {
  list: () => api.get('/projects'),
  create: (payload) => api.post('/projects', payload),
  update: (id, payload) => api.patch(`/projects/${id}`, payload),
  remove: (id) => api.delete(`/projects/${id}`),
}

export const taskApi = {
  list: () => api.get('/tasks'),
  create: (payload) => api.post('/tasks', payload),
  update: (id, payload) => api.patch(`/tasks/${id}`, payload),
  remove: (id) => api.delete(`/tasks/${id}`),
}

export const dashboardApi = { get: () => api.get('/dashboard') }
