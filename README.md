# AI Agent with LangGraph

An intelligent, stateful AI Agent built with **LangGraph** and **FastAPI** that can handle complex conversations, use tools, and maintain across interactions. Features PostgreSQL based checkpointing for production-ready reliability.

## Features

- **Stateful Conversations**: Maintains conversation history and context using LangGraph checkpoints 
- **Tool Usage**: Agent can dynamically use tools to complete tasks.
- **Persistent Memory**: PostgreSQL-based state management survives server restarts
- **Async-First**: Built with FastAPI for high-performance, non-blocking operations
- **Production-Ready**: Fully Dockerized with proper lifespan management 
- **Conversation Tracking**: Full message history with tool call visibility 

--

## How It Works 

The agent uses **LangGraph's StateGraph** architecture:

1. **Graph-Based Flow**: Conversation flow through nodes (tools, LLM, memory) in a controlled graph
2. **Checkpointing**: Every state change is saved to PostgreSQL, enabling:
   -Conversation resumption after memory
   -Multi-turn conversation memory 
   -Audit trails of agent decisions 
3. **Tool Calling**: Agent intelligently decided when to use tools based on user requests 
4. **Async Processing**: Non-blocking I/O for handling multiple concurrent conversations 

--

## Configuration

| Setting | Value | Description |
|-----|-----|-----------|
| **Framework** | LangGraph | Graph-based agent orchestration |
| **LLM Model** | 'gemini-3.5-flash-lite' | Google's Gemini for reasoning |
| **Security** | HS256 + JWT | Token-based authentication |
| **Checkpoint Backend** | PostgreSQL | Persistent state storage |
| **API Framework** | FastAPI | High-performance async API |
| **Memory Type** | Persistent | Survives server restarts |

--

## Tech Stack 

- **Agent Framework**: LangGraph (LangChain)
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL (for checkpoints & state)
- **Containerization**: Docker & Docker Compose 
- **LLM**: Google Gemini API 

--

## prerequisites

-[Docker Desktop]*(https://www.docker.com/products/docker-desktop/)*
-[Git]*(https://git-scm.com/)*
-Google API Key (for Gemini)

--

## Installation & Setup 

### 1. Clone the repository 
```bash
git clone https://github.com/YOUR_USERNAME/ai_agent_support.git
cd ai_agent_suppport
```

### 2. Configure Environment Variables 

**Step A: Generate a Secure Secret Key**
Run this command in your terminal 
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

*Copy the long string that gets printed out.*

**Step B: Create the '.env' File**
Create a '.env' file in the root directory:

```env
# Database Configuration 
DATABASE_URL=postgresql://admin:YOUR_PASSWORD@db:5432/ai_agent_db
 
#AI Configuration 
GOOGLE_API_KEY=your_google_api_key_here
LLM_MODEL_NAME=gemini-3.5-flash-lite
EMBEDDING_MODEL_NAME=gemini-embedding-001

#Security Configurtion (for JWT authentication)
SECRET_KEY=paste_the_generated_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=1440
 
#Server Configuration 
HOST=0.0.0.0
PORT=8000

*(Replace 'your_google_api_key_here' with your real Google AI Studio API Key, and paste your generated key into 'SECRET_KEY')*
```

### 3. Run With Docker
```bash
docker-compose up --build -d 
```

### 4. Access the API 
Open your browser:
**http://localhost:8000/docs**

--

## Project Structure 

ai-agent-project/
├── ai/                     # Agent core logic
│   ├── init.py
│   ├── brain.py           # Creates agent graph
│   ├── tools.py           # Agent tools (search, calc, etc.)
│   ├── ask_question.py    # Question handling
│   └── file_upload.py     # File processing
├── core/                   # Config & security
├── db/                     # Database models
├── routers/                # API endpoints
├── docker-compose.yml      # Docker orchestration
├── Dockerfile             # Python environment
├── init.sql               # DB initialization
├── main.py                # FastAPI app with lifespan
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables

-- 

## API Endpoints

- **POST /chat** - Send a message to the agent 
- **POST /chat/with-tools** - Send a message with tool access 
- **GET /health** - Check the server is running 
- **GET /conversations/{user_id}** - Retrieve conversation history 

*(Check '/docs' for full interactive API documentation)*

--

## Testing the Agent 

**Example 1: Simple Question**
```bash 
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d'{"user_id": "user123", "message": "what is the weather today?"}'
```

**Example 2: Using Tools**
```bash
curl -X POST "http://localhost:8000/chat/with-tools" \
  -H "Content-Type: application/json"
  -d'{"user_id": "user123", "message": "Search for Python tutorials"}
```

--

## Managing the Application 

**Stop (preserves data)** 
```bash 
docker-compose down 
```

**Stop and wipe (delete all conversations): 
```bash
docker-compose down -v
```

**View logs:**
```bash
docker-compose logs -f
```

--
