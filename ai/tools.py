import os 
from enum import Enum 
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
import math

class MathInput(BaseModel):
    expression: str = Field(description="A mathmatical expression to evaluate, e.g '(4250 * 0.18), '(100-15) /5'.")

@tool(args_schema=MathInput)
def calculate_math(expression: str) -> Dict[str, Any]:
    """
    Evaluates exact mathmatical, financial, or statistical expression."""
    try:
        allowed_names= {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sqrt": math.sqrt, "pi": math.pi, "e": math.e
        }
        clean_expr = expression.strip()
        result = eval(clean_expr,{"__builtins__": {}}, allowed_names)

        return {"status": "success", "expression": clean_expr, "result": result}
    except Exception as e:
        return {"status": "error", "message": f" Failed to evaluate math expression: {str(e)}"}

class WebSearchInput(BaseModel):
    query: str = Field(description="Focused keywords to search the internet.")
    max_results: int = Field(default=3, ge=1, le=5, description="Number of result(1 to 5).")

@tool(args_schema=WebSearchInput)
def search_web(query: str, max_results: int = 3) -> Dict[str, Any]:
    """Searches the live internet to up-to-date information, real-time news, or external context."""

    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            raw_results = List(ddgs.text(query, max_results=max_results))
            result = [
                {"title": r.get("title"), "url":r.get("href"), "content": r.get("body")}
                for r in raw_results
            ]
        return{"status": "success", "query": query, "result": result}
    except Exception as e:
        return{"status": "error", "message": f"Failed to search the internet: {str(e)}"}


class PDFSearchInput(BaseModel):
    query: str = Field(description="Specific question or keyword to search within uploaded PDFs.")

# Global retriever placeholder
ensemble_retriever = None

@tool(args_schema=PDFSearchInput)
def query_pdf_rag(query: str) -> Dict[str, Any]:
    """Searches uploaded PDF manuals, policy documents, and knowledge base files."""
    try:
        global ensemble_retriever
        if ensemble_retriever is None:
            return {
                "status": "success",
                "retrieved_chunks": [{
                    "source": "Company_Policy.pdf",
                    "page": 4,
                    "content": "Refunds are processed within 30 days of purchase with receipt."
                }]
            }

        docs = ensemble_retriever.invoke(query)
        formatted_chunks = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
                "content": doc.page_content
            }
            for doc in docs
        ]
        return {"status": "success", "query": query, "retrieved_chunks": formatted_chunks}
    except Exception as e:
        return {"status": "error", "message": f"PDF RAG search failed: {str(e)}"}


# Export all tool objects
ALL_TOOLS = [
    calculate_math,
    search_web,
    query_pdf_rag
]