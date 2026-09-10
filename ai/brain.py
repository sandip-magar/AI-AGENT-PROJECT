import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.graph import StateGraph, START, END 
from langgraph.prebuilt import ToolNode 
from ai.tools import search_web, calculate_math, query_pdf_rag, ALL_TOOLS
from langchain_postgres import PGVector
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage

load_dotenv()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
COLLECTION_NAME = "my_pdf_files"
embedding = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME)
DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#SET UP THE VECTORSTORE 
vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    embeddings=embedding,
    connection=DATABASE_URL
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0.5, google_api_key=GOOGLE_API_KEY)
llm_with_tools = llm.bind_tools(ALL_TOOLS)
tool_node = ToolNode(ALL_TOOLS)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def retrieve_documents(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    docs = retriever.invoke(last_message.content)

    context = "\n\n".join(doc.page_content for doc in docs)

    system_messages = SystemMessage(content="""
    You are a helpful AI assistant.

    IMPORTANT RULES:
    1. Give DIRECT and CONCISE answers. Don't explain unless asked.
    2. For simple questions (math, facts, definition), just give the answer.
    3. PDF priority (HIGHEST). Always check the 'PDF Context' below FIRST. if the answer is in the PDF. DO NOT USE web search.
    4. ONLY use 'web_search' for real-time news, weather, or general knowledge NOT in the PDF.
    5. Only provide detailed explanations if the user explicity asks "explain", "how", or "why".

    PDF Context:
    {context}
    
    User Question: {last_message.content}
    """)

    return {"messages": [system_messages]}

def agent_call(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

def create_agent_graph(checkpointer=None):

    workflow = StateGraph(AgentState)
    
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("agent", agent_call)
    workflow.add_node("tools", tool_node)

    #Set the entry point 
    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "agent")

    #Set the conditional edge 
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    workflow.add_edge("tools", "agent")

    #compile the graph 
    return workflow.compile(checkpointer=checkpointer)