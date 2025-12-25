# Physical AI & Humanoid Robotics

An interactive educational book on Physical AI and Humanoid Robotics, built with Docusaurus and featuring an AI-powered RAG chatbot, content personalization, and Urdu translation.

## Live Demo

- **Book Site:** [https://saghir-abbasi.github.io/book_project/](https://saghir-abbasi.github.io/book_project/)

## Features

### Core Features

- **Interactive Book Platform**: A comprehensive guide to Physical AI and Humanoid Robotics built with Docusaurus
- **RAG Chatbot**: AI-powered chatbot that answers questions about book content using Retrieval-Augmented Generation
- **User Authentication**: Secure signup/signin with session-based authentication
- **User Preferences**: Store and apply user background preferences (Software/Hardware) for personalized content

### Bonus Features

- **Content Personalization**: Adapts chapter content based on user's background (Software Developer or Hardware Engineer)
- **Urdu Translation**: Translates chapter content to Urdu with proper RTL rendering and Nastaliq font support
- **Protected Reading**: Auth-gated access to book content with seamless modal-based authentication

## Book Content

The book is organized into 4 modules with 8 chapters:

### Module 1: Robotic Nervous System
- Chapter 1: ROS2 Basics
- Chapter 2: URDF Fundamentals

### Module 2: Digital Twin
- Chapter 1: Gazebo Physics
- Chapter 2: Unity Simulation

### Module 3: AI Robot Brain
- Chapter 1: Isaac Sim Basics
- Chapter 2: VSLAM Navigation

### Module 4: Vision Language Action
- Chapter 1: Cognitive Planning
- Chapter 2: Whisper Integration

## Tech Stack

### Frontend (Docusaurus Book Site)
- **Framework**: Docusaurus 3.x
- **Language**: TypeScript / React
- **Styling**: CSS Modules
- **Auth**: Session-based with HTTP-only cookies
- **Deployment**: GitHub Pages

### Backend (FastAPI)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: Neon Serverless PostgreSQL
- **Vector Store**: Qdrant Cloud
- **AI**: OpenAI Agents SDK
- **Auth**: Session-based with bcrypt password hashing

## Project Structure

```
book_ai_robotics/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API routes (chat, embed, query)
│   │   ├── app/agent/         # OpenAI Agent integration
│   │   ├── auth/              # Authentication module
│   │   ├── core/              # Embeddings and core logic
│   │   ├── db/                # Database and Qdrant clients
│   │   └── models/            # SQLAlchemy models
│   ├── tests/                 # Unit and integration tests
│   └── requirements.txt
│
├── docusaurus-book-site/      # Docusaurus frontend
│   ├── docs/book-content-internal/
│   │   └── modules/           # Book chapters (MDX)
│   ├── src/
│   │   ├── auth/              # Auth context and hooks
│   │   ├── components/
│   │   │   ├── Auth/          # Auth components
│   │   │   ├── ChapterToolbar/ # Personalize/Translate buttons
│   │   │   └── chatbot/       # RAG chatbot widget
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Auth pages
│   │   └── theme/             # Custom Docusaurus theme
│   └── docusaurus.config.ts
│
├── specs/                     # Feature specifications
├── history/                   # Prompt history records
└── .specify/                  # Spec-Kit Plus configuration
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or Neon Serverless)
- Qdrant Cloud account
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/database
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   OPENAI_API_KEY=your-openai-api-key
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. Navigate to the docusaurus site:
   ```bash
   cd docusaurus-book-site
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

4. Open [http://localhost:3000/book_project/](http://localhost:3000/book_project/)

### Deployment

#### Frontend (GitHub Pages)

```bash
cd docusaurus-book-site
npm run build
npm run deploy
```

#### Backend (Vercel/Railway/etc.)

Deploy the backend to your preferred platform with the environment variables configured.

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/signin` - Sign in
- `POST /api/auth/signout` - Sign out
- `GET /api/auth/session` - Get current session
- `PUT /api/auth/user/preference` - Update user preferences

### Chatbot
- `POST /chat/` - Send a message to the chatbot
- `GET /chat/history/{session_id}` - Get chat history

### Embeddings
- `POST /embed/chapter` - Embed chapter content
- `POST /embed/batch` - Batch embed multiple chapters

### Query
- `POST /query/search` - Search for relevant content
- `POST /query/ask` - Ask a question about the book

### Agent
- `POST /api/agent/chat` - Stream chat with OpenAI Agent

## Development Tools

This project was built using:
- **Claude Code**: AI-powered code agent
- **Spec-Kit Plus**: Specification-driven development toolkit

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is created for the PIAIC Quarter 4 hackathon.

## Author

**Saghir Abbasi**

---

Built with Docusaurus and powered by AI
