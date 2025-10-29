import axios from 'axios';
import { User, Message, MessageWithUsers, OnlineUser } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  
  register: async (username: string, email: string, password: string) => {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data;
  },
  
  getMe: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Users API
export const usersAPI = {
  getOnlineUsers: async (): Promise<OnlineUser[]> => {
    const response = await api.get('/users/online');
    return response.data;
  },
  
  getAllUsers: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
  },
  
  getUser: async (userId: number): Promise<User> => {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  },
};

// Messages API
export const messagesAPI = {
  sendMessage: async (content: string, receiverId: number): Promise<MessageWithUsers> => {
    const response = await api.post('/messages', { content, receiver_id: receiverId });
    return response.data;
  },
  
  getConversation: async (userId: number, skip = 0, limit = 50): Promise<MessageWithUsers[]> => {
    const response = await api.get(`/messages/conversation/${userId}?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  
  searchMessages: async (query: string, skip = 0, limit = 50): Promise<MessageWithUsers[]> => {
    const response = await api.get(`/messages/search?q=${encodeURIComponent(query)}&skip=${skip}&limit=${limit}`);
    return response.data;
  },
  
  markMessageRead: async (messageId: number): Promise<void> => {
    await api.put(`/messages/${messageId}/read`);
  },
  
  getUnreadCount: async (): Promise<{ unread_count: number }> => {
    const response = await api.get('/messages/unread-count');
    return response.data;
  },
};

export default api;
