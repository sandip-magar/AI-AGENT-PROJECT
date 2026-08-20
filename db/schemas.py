from pydantic import BaseModel, Field
from datetime import datetime 
from typing import Optional, Annotated, TypedDict, List
from langgraph.graph.message import add_messages

class UserCreate(BaseModel):
    username: str 
    password: str
    is_active: bool = True

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None 

class UserResponse(BaseModel):
    id: int 
    username: str
    is_active : bool = True
    created_at : datetime

    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token: str 
    token_type: str

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

class AskQuestion(BaseModel):
    question: str

class AskAIRequest(BaseModel):
    thread_id : str = Field(..., description="Unique identifier for the chat thread")
    message: str = Field(..., description="The User Query")

class AskAIResponse(BaseModel):
    thread_id: str 
    response: str