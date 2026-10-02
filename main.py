from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from routers.users import router as user_router
from routers.auth import router as auth_router
from fastapi.exceptions import RequestValidationError
from core.extension import http_exception_handler, validation_error_handler, Server_error_handler
from ai.file_upload import router as file_upload_router
from ai.ask_question import router as ask_router
from chat.chat_history import router as chat_router
import os 
from dotenv import load_dotenv
from ai.brain import create_agent_graph
from contextlib import asynccontextmanager
load_dotenv()

checkpointer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global checkpointer
    print("Starting up the application...")
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    DATABASE_URL = os.getenv("DATABASE_URL")
    async with AsyncPostgresSaver.from_conn_string(DATABASE_URL + "?prepare_threshold=0") as checkpointer:

        await checkpointer.setup()

        app.state.agent_graph = create_agent_graph(checkpointer=checkpointer)

        print("Server is ready! AI Agent is loaded.")
        yield #Server runs here

        print('Shutting down')

app = FastAPI(lifespan=lifespan)



app.include_router(auth_router, prefix="/users", tags=['Authentication'])
app.include_router(user_router, prefix="/users", tags=["User Handle"])

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, Server_error_handler)

app.include_router(file_upload_router, prefix="/ai", tags=["Handle PDF-File"])
app.include_router(ask_router, prefix="/ai", tags=["Ask Question"])

app.include_router(chat_router, prefix="/chat", tags=["Clean-Chat-History"])