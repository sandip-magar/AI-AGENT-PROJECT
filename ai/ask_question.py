from db.database import get_db
from sqlalchemy.orm import Session 
from db.models import User, ChatMessage
from fastapi import APIRouter, Depends, HTTPException, status, Request
from langchain_core.messages import HumanMessage, SystemMessage
from db.schemas import AskQuestion
from routers.auth import get_current_user

router = APIRouter()

@router.post("/ask-ai")
async def ask_ai(
    request: Request,
    payload: AskQuestion,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    graph = request.app.state.agent_graph

    thread_id = f"user_{current_user.id}"
    config = {"configurable": {"thread_id": thread_id}}


    #Prepare the input for the agent graph
    inputs = {"messages": [HumanMessage(content=payload.question)]}

    try:
        final_state = await graph.ainvoke(
            inputs,
            config=config
            )
        
        #Extract the response from the final state
        raw_response = final_state["messages"][-1].content
        ai_response = str(raw_response)

        #Save to SQL Database
        user_msg = ChatMessage(role="user", content=payload.question, user_id=current_user.id)
        ai_msg = ChatMessage(role="assistant", content=ai_response, user_id=current_user.id)
        
        db.add(user_msg)
        db.add(ai_msg)
        db.commit()

        return {
            "success": True,
            "thread_id": thread_id,
            "answer": ai_response
            }
    except KeyError as e:
        print(f"KeyError: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"KeyError: {e}"
        )
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )