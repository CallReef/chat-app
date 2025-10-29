'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useChat } from '@/contexts/ChatContext';
import { UserList } from './UserList';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { LogOut, Search } from 'lucide-react';
import { Message, OnlineUser } from '@/types';

export const ChatApp: React.FC = () => {
  const { user, logout } = useAuth();
  const { 
    onlineUsers, 
    currentChatUser, 
    setCurrentChatUser, 
    messages,
    typingUsers,
    searchMessages 
  } = useChat();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Message[]>([]);
  const [showSearch, setShowSearch] = useState(false);

  const handleUserSelect = (user: OnlineUser) => {
    setCurrentChatUser(user);
  };

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const results = await searchMessages(query);
      setSearchResults(results);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  useEffect(() => {
    if (searchQuery) {
      const timeoutId = setTimeout(() => {
        handleSearch(searchQuery);
      }, 300);
      return () => clearTimeout(timeoutId);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  if (!user) {
    return null;
  }

  return (
    <div className="h-screen flex bg-gray-100">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-indigo-500 rounded-full flex items-center justify-center text-white font-medium">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">{user.username}</h1>
                <p className="text-sm text-gray-500">Online</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowSearch(!showSearch)}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <Search className="w-5 h-5" />
              </button>
              <button
                onClick={logout}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Search */}
        {showSearch && (
          <div className="p-4 border-b border-gray-200">
            <input
              type="text"
              placeholder="Search messages..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            {searchResults.length > 0 && (
              <div className="mt-2 space-y-1">
                {searchResults.slice(0, 5).map((result) => (
                  <div key={result.id} className="p-2 bg-gray-50 rounded text-sm">
                    <p className="truncate">{result.content}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(result.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* User List */}
        <UserList
          onlineUsers={onlineUsers}
          onUserSelect={handleUserSelect}
          selectedUserId={currentChatUser?.id}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <MessageList
          messages={messages}
          currentUser={user}
          currentChatUser={currentChatUser}
          typingUsers={typingUsers}
        />
        <MessageInput
          currentChatUser={currentChatUser}
          currentUser={user}
        />
      </div>
    </div>
  );
};
