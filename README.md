# AI Agent with LangGraph & FastAPI 

An intelligent, stateful AI agent that can execute tools, maintain conversation memory, and perform real-time web searches, Built with FastAPI, LangGraph, PostgreSQL, and Docker.

[![FastAPI](https://img.shields.io/badge/FastAPI=0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads)
[![Docker](https://img.shields.io/badge/docker-compose-3.8-blue.svg)](https://docs.docker.com/compose/)

## Features

- **Stateful AI Agent**: Powered by LangGraph with persistent memeory using PostgreSQL checkpoints
- **Custom Tools**: Web search, mathematical calculations, and PDF RAG with strict Pydantic validation 
- **User Authentication**: JWT-based auth with secure passwordd hashing
- **Chat History**: Full conversation tracking with thread-based session management 
- **PDF Uploads & RAG**: Semantic search through uploaded documents using pgvector 
- **Dockerized**: Production-ready containerization with docker-compose 
- **Tested**: Comprehensive pytest test suite for tools and API endpoints 

## Architecture 

This project implements a **RAG(Retrieval-Augmented Generation)** architecture with:
- **FastAPI** for high-performance async API endpoints
- **LangGraph** for cyclical, stateful agent workflows 
- **PostgreSQL + pgvector** for both relational data and vector embeddings 
- **Gemini API** for LLM inference and embeddings

## Project Structure 
```
ai-agent-project/
├── ai/                          # AI Agent Core Logic
│   ├── init.py
│   ├── brain.py                 # LangGraph agent creation
│   ├── tools.py                 # Custom tools with Pydantic validation
│   ├── ask_question.py          # Question handling logic
│   └── file_upload.py           # PDF processing & chunking
├── chat/                        # Chat History Management
│   ├── init.py
│   └── chat_history.py          # Get/delete conversation history
── core/                        # Configuration & Security
│   ├── init.py
│   ├── config.py                # Environment variables
│   ├── security.py              # JWT, password hashing
│   └── extensions.py            # Logging & middleware
├── db/                          # Database Layer
│   ├── init.py
│   ├── database.py              # Database connection & session
│   ├── models.py                # SQLAlchemy models
│   └── schemas.py               # Pydantic schemas
── routers/                     # API Endpoints
│   ├── init.py
│   ├── auth.py                  # Register, login, auth routes
│   └── users.py                 # User CRUD operations
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Python 3.11 environment
├── init.sql                     # Database initialization
├── main.py                      # FastAPI app with lifespan
├── requirements.txt             # Python dependencies
├── test_tools.py                # Pytest unit tests
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

## Quick Start 

### Prerequisites 
Before you begin, ensure you have the following installed on your computer.

* **[Docker & Docker Compose]*(https://docker.com/products/docker-desktop/)*** -Required to run the database and API containers.
* **[GitHub]*(https://git-scm.com/downloads)*** - To clone the repository 
* **[Google Gemini API Key]*(https://aistudio.google.com/app/apikey)*** - Required for the AI agent to think and generate embeddings.

### Installation 

1. **Clone the repository**
git clone https://github.com/sandip-magar/AI-AGENT-PROJECT.git
- cd AI-AGENT-PROJECT

2. **Create environment file:**
```bash
cp.env.example .env
#Edit .env with your credentials 
```

4. **Access the API:**
- Swagger UI: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

## Docker Management Commands 

**Stop the containers (Keeps database data):**
```bash
docker-compose down 
```

**Stop and completely reset the database(Deletes all data):**
```bash
docker-compose down -v
```

**View real-time server logs (Great for debugging):**
```bash
docker-compose logs -f 
```

**Rebuild the app after you make code changes:**
```bash
docker-compose up --build -d
```

## Running Tests

```bash 
#Run all tests
pytest 

#Run with verbose output 
pytest -v

#Run specific test file 
pytest test_tools.py 
```

## API Endpoints 

### Authentication 
- `POST /register` - Create new user account 
- `POST /login` - Authenticate and receive JWT token 
- `GET / users/{user_id}` - Get user profile 
- `PUT /users/{user_id}` - Update user profile 
- `DELETE /users/{user_id}` - Delete user account 

### File Upload
- `POST /upload-pdf` - Upload PDF for RAG
- `GET / documents` - List uploded documents
- `DELETE documents/{doc_id}` - Delete document

## Environment Variables 

Create a `.env` file in the root dictory: 

```env 
#Database 
POSTGRES_USER=admin 
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ai_agent_db
DATABASE_URL=postgresql://agmin:your_password@db:5432/ai_agent_db

#Security 
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=1440

#AI
GOOGLE_API_KEY=your_gemini_key_here
LLM_MODEL_NAME=gemini-pro
EMBEDDING_MODEL_NAME=gemini-embedding-001

#Application 
ENVIRONMENT=development
```

## Tools
The AI agent has access to these validated tools: 
1. **Web Search** - Real-time internet search via DuckDuckGo
2. **Math Calculator** - Secure mathematical expressions with sandboxed eval 
3. **PDF RAG** - Sementic search through uploaded documents

All tools use **pydantic schemas** for strict input validation to prevent AI hallucinations and security vulnerabilites.

## LangGraph Architecture 

The agent uses a **ReAct (Reason + Act)** pattern:
1. **Reason**: LLM analyzes the user query 
2. **Act**: Decides whether to use a tool or respond directly 
3. **Observe**: Processes tool output 
4. **Repeat**: Loops until final answer final answer is generated 

State is persisted in PostgreSQL using `AsyncPostgresSaver`, enabling:
- Conversation continuity across requests 
- Muli-turn tool usage
- Recovery from interruptions 

## Database Schema 

- **users** - User accounts with hashed passwords 
- **pdf_documents** - Uploaded PDFs with embeddings (3072-dim vectors)
- **chat_messages** - Conversation history with thread IDs 
- **langgraph checkpoints** - Agent state persistence

## Security Features 

- Password hashing with bcrypt 
- JWT token authentication 
- CORS configuration 
- SQL injection preventing via SQLAlchemy ORM 
- Tool input validation with Pydantic 
- sandboxed math evaluation (whitelisted functions only)

## Production Deployment

For production deployment 

1. set `ENVIRONMENT=production` in `.env`
2. Use strong, unique `SECRET_KEY`
3. Configure CORS origins properly 
4. Set up HTTPS/TLS 
5. Use a production WSGI server (Gunicorn + Uviorn workers)
6. Configure database connection pooling 
7. Set up monitoring and logging 

## Author
**Sandip Magar**
[GitHub]*(https://github.com/sandip-magar)

--

**Built with ❤️ using FastAPI, LangGraph, and PostgreSQL**