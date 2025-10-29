# Chat App - Real-time Messaging

A full-stack real-time chat application built with FastAPI, Next.js, and Redis. This project demonstrates modern web development practices with real-time communication, authentication, and scalable architecture.

## ✨ Features

### Core Features
- **Real-time messaging** with WebSockets
- **JWT-based authentication** with secure login/register
- **Redis pub/sub** for message broadcasting
- **PostgreSQL** for message persistence
- **Modern Next.js frontend** with Tailwind CSS
- **Typing indicators** ("User is typing...")
- **Read receipts** (✓✓ like WhatsApp)
- **Message search** functionality
- **In-app notifications** with toast messages
- **Online user status** tracking
- **Responsive design** for mobile and desktop

### Advanced Features
- **WebSocket reconnection** with exponential backoff
- **Message history** with pagination
- **Real-time user presence** updates
- **Typing indicators** via Redis pub/sub
- **Message search** across all conversations
- **Unread message counts**
- **Modern UI/UX** with Tailwind CSS

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **WebSockets** - Real-time communication
- **Redis** - Pub/sub messaging and caching
- **PostgreSQL** - Reliable data persistence
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **JWT** - Secure authentication
- **Pydantic** - Data validation

### Frontend
- **Next.js 16** - React framework with App Router and component caching
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **WebSocket API** - Real-time communication
- **React Context** - State management
- **Axios** - HTTP client
- **React Hot Toast** - Notifications
- **Lucide React** - Beautiful icons

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local development
- **GitHub Actions** - CI/CD pipeline
- **Railway** - Backend deployment
- **Vercel** - Frontend deployment

## 🏃‍♂️ Quick Start

### Prerequisites
- **Bun** (recommended) or Node.js 18+
- **Python 3.11+**
- **Docker** and **Docker Compose**
- **PostgreSQL** and **Redis** (or use Docker)

### Option 1: Docker Compose (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd chat-app

# Start all services
docker-compose up -d

# Initialize database with sample data
docker-compose exec backend python init_db.py
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Install dependencies
bun install

# Set up environment
cp .env.example .env
# Edit .env with your database and Redis URLs

# Start PostgreSQL and Redis (or use Docker)
# Create database: createdb chat_app

# Run migrations
alembic upgrade head

# Initialize with sample data
python init_db.py

# Start development server
bun run dev
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
bun install

# Start development server
bun run dev
```

## 🎯 Demo Accounts

The app comes with pre-loaded demo accounts for easy testing:

- **alice** / password123
- **bob** / password123  
- **charlie** / password123

## 📁 Project Structure

```
chat-app/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── routers/            # API route handlers
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication logic
│   ├── websocket_manager.py # WebSocket handling
│   ├── redis_client.py     # Redis operations
│   ├── main.py             # FastAPI app
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── lib/           # Utilities and API client
│   │   └── types/         # TypeScript types
│   └── package.json       # Node.js dependencies
├── docker-compose.yml      # Local development setup
├── .github/workflows/      # CI/CD pipeline
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Users
- `GET /users` - Get all users
- `GET /users/online` - Get online users
- `GET /users/{user_id}` - Get specific user

### Messages
- `POST /messages` - Send message
- `GET /messages/conversation/{user_id}` - Get conversation
- `GET /messages/search` - Search messages
- `PUT /messages/{message_id}/read` - Mark as read
- `GET /messages/unread-count` - Get unread count

### WebSocket
- `WS /ws/{token}` - Real-time messaging

## 🚀 Deployment

### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set environment variables:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `SECRET_KEY`
   - `FRONTEND_URL`
3. Deploy automatically on push to main

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_WS_URL`
3. Deploy automatically on push to main

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests
cd frontend
bun run test
```

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with React

## 📈 Performance Features

- Redis caching for online users
- WebSocket connection pooling
- Message pagination
- Lazy loading of components
- Optimized bundle size with Next.js 16
- Component caching for enhanced performance
- Fast builds with webpack (Turbopack disabled for stability)

## 🔧 Troubleshooting

### Common Issues

#### Turbopack Errors in Next.js 16
If you encounter Turbopack internal errors, the project is configured to use webpack instead for stability:

```bash
# If you see Turbopack errors, restart the frontend
cd frontend
rm -rf .next
bun run dev
```

#### Port Already in Use
```bash
# Kill processes using ports 3000 and 8000
lsof -ti:3000,8000 | xargs -r kill -9

# Then restart services
cd backend && source venv/bin/activate && python main.py &
cd frontend && bun run dev &
```

#### Python Module Not Found
```bash
# Make sure you're using the virtual environment
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Database Connection Issues
```bash
# Start PostgreSQL and Redis with Docker
docker-compose up -d postgres redis

# Or install locally and ensure services are running
```

### Development Tips

- **Backend**: Always activate the virtual environment before running Python commands
- **Frontend**: Use `bun` for faster package management
- **Database**: Use Docker Compose for consistent local development
- **WebSockets**: Check browser console for connection issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎉 Why This Project Impresses

This chat application demonstrates several advanced concepts that are highly valued in the industry:

- **Real-time Communication**: WebSockets and Redis pub/sub
- **Scalable Architecture**: Microservices with proper separation
- **Modern Tech Stack**: Latest versions of popular frameworks
- **Production Ready**: Docker, CI/CD, and deployment configs
- **Developer Experience**: TypeScript, hot reload, and good tooling
- **User Experience**: Responsive design and real-time features

Perfect for showcasing your full-stack development skills! 🚀
