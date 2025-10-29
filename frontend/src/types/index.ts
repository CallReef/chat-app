export interface User {
  id: number;
  username: string;
  email: string;
  is_online: boolean;
  created_at: string;
}

export interface Message {
  id: number;
  content: string;
  sender_id: number;
  receiver_id: number;
  is_read: boolean;
  created_at: string;
  sender?: User;
  receiver?: User;
}

export interface MessageWithUsers extends Message {
  sender: User;
  receiver: User;
}

export interface OnlineUser {
  id: number;
  username: string;
  is_online: boolean;
}

export interface TypingIndicator {
  user_id: number;
  username: string;
  is_typing: boolean;
  chat_partner_id: number;
}

export interface WebSocketMessage {
  type: 'message' | 'user_status' | 'online_users' | 'typing';
  [key: string]: unknown;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

export interface ChatContextType {
  messages: Message[];
  onlineUsers: OnlineUser[];
  currentChatUser: OnlineUser | null;
  typingUsers: Set<number>;
  sendMessage: (content: string, receiverId: number) => Promise<void>;
  setCurrentChatUser: (user: OnlineUser | null) => void;
  sendTypingIndicator: (isTyping: boolean, chatPartnerId: number) => void;
  searchMessages: (query: string) => Promise<Message[]>;
}
