'use client';

import React from 'react';
import { OnlineUser } from '@/types';
import { User, MessageCircle } from 'lucide-react';

interface UserListProps {
  onlineUsers: OnlineUser[];
  onUserSelect: (user: OnlineUser) => void;
  selectedUserId?: number;
}

export const UserList: React.FC<UserListProps> = ({ 
  onlineUsers, 
  onUserSelect, 
  selectedUserId 
}) => {
  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Online Users</h2>
        <p className="text-sm text-gray-500">{onlineUsers.length} online</p>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {onlineUsers.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            <User className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2">No users online</p>
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {onlineUsers.map((user) => (
              <button
                key={user.id}
                onClick={() => onUserSelect(user)}
                className={`w-full flex items-center p-3 rounded-lg text-left transition-colors ${
                  selectedUserId === user.id
                    ? 'bg-indigo-100 text-indigo-900'
                    : 'hover:bg-gray-100 text-gray-900'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <div className="w-10 h-10 bg-indigo-500 rounded-full flex items-center justify-center text-white font-medium">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{user.username}</p>
                    <p className="text-xs text-gray-500">Online</p>
                  </div>
                  <MessageCircle className="w-4 h-4 text-gray-400" />
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
