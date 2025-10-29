'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Message, OnlineUser, User, ChatContextType, WebSocketMessage } from '@/types';
import { messagesAPI, usersAPI } from '@/lib/api';
import { wsManager } from '@/lib/websocket';
import { useAuth } from './AuthContext';

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<OnlineUser[]>([]);
  const [currentChatUser, setCurrentChatUser] = useState<OnlineUser | null>(null);
  const [typingUsers, setTypingUsers] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (!user) return;

    // Load online users
    loadOnlineUsers();

    // Set up WebSocket message handlers
    const handleMessage = (data: WebSocketMessage) => {
      if (data.type === 'message') {
        const message = data as unknown as Message;
        setMessages(prev => [message, ...prev]);
      }
    };

    const handleUserStatus = (data: WebSocketMessage) => {
      if (data.type === 'user_status') {
        setOnlineUsers(prev => {
          const filtered = prev.filter(u => u.id !== (data.user_id as number));
          if (data.is_online) {
            return [...filtered, { 
              id: data.user_id as number, 
              username: data.username as string, 
              is_online: true 
            }];
          }
          return filtered;
        });
      }
    };

    const handleOnlineUsers = (data: WebSocketMessage) => {
      if (data.type === 'online_users') {
        setOnlineUsers(data.users as OnlineUser[]);
      }
    };

    const handleTyping = (data: WebSocketMessage) => {
      if (data.type === 'typing') {
        setTypingUsers(prev => {
          const newSet = new Set(prev);
          if (data.is_typing) {
            newSet.add(data.user_id as number);
          } else {
            newSet.delete(data.user_id as number);
          }
          return newSet;
        });
      }
    };

    wsManager.onMessage('message', handleMessage);
    wsManager.onMessage('user_status', handleUserStatus);
    wsManager.onMessage('online_users', handleOnlineUsers);
    wsManager.onMessage('typing', handleTyping);

    return () => {
      wsManager.removeMessageHandler('message', handleMessage);
      wsManager.removeMessageHandler('user_status', handleUserStatus);
      wsManager.removeMessageHandler('online_users', handleOnlineUsers);
      wsManager.removeMessageHandler('typing', handleTyping);
    };
  }, [user]);

  const loadOnlineUsers = async () => {
    try {
      const users = await usersAPI.getOnlineUsers();
      setOnlineUsers(users);
    } catch (error) {
      console.error('Error loading online users:', error);
    }
  };

  const sendMessage = async (content: string, receiverId: number) => {
    try {
      const message = await messagesAPI.sendMessage(content, receiverId);
      setMessages(prev => [message, ...prev]);
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  };

  const loadConversation = async (userId: number) => {
    try {
      const conversationMessages = await messagesAPI.getConversation(userId);
      setMessages(conversationMessages.reverse()); // Reverse to show oldest first
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const searchMessages = async (query: string): Promise<Message[]> => {
    try {
      const results = await messagesAPI.searchMessages(query);
      return results;
    } catch (error) {
      console.error('Error searching messages:', error);
      return [];
    }
  };

  const sendTypingIndicator = (isTyping: boolean, chatPartnerId: number) => {
    wsManager.sendTypingIndicator(isTyping, chatPartnerId);
  };

  const value: ChatContextType = {
    messages,
    onlineUsers,
    currentChatUser,
    typingUsers,
    sendMessage,
    setCurrentChatUser,
    sendTypingIndicator,
    searchMessages,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};
