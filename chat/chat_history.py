from fastapi import APIRouter, HTTPException, status, Depends
from routers.auth import get_current_user
from db.database import get_db
from db.models import User, ChatMessage
from sqlalchemy.orm import Session
from sqlalchemy import desc, text 

router = APIRouter()

@router.get("/")
async def get_user_history(
    limit: int = 10,
    skip: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_message = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(desc(ChatMessage.created_at)).offset(skip).limit(limit).all()
    return chat_message


@router.delete("/chat-history") 
async def delete_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete ALL chat history for the current user:
    1. ChatMessages table
    2. Langgraph checkpoints(AI memory)"""

    print(f"Deleting chat history for user {current_user.id}")

    try: 
        #Delete from ChatMessage database
        db.query(ChatMessage).filter(
            ChatMessage.user_id == current_user.id
        ).delete()
        db.commit()

        #Delete from the langgraph checkpoints
        thread_id = f"user_{current_user.id}"

        from db.database import engine 

        with engine.connect() as conn:
            #Delete from checkpoints
            conn.execute(
                text("DELETE FROM checkpoints WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            )

            #Delete from checkpoint_blobs
            conn.execute(
                text("DELETE FROM checkpoint_blobs WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            )

            #Delete from checkpoints_writes
            conn.execute(
                text("DELETE FROM checkpoint_writes WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            )
            conn.commit()

            print(f" Chat history deleted for user {current_user.id}")

            return {
                "success": True,
                "message": "ALL chat history and AI memory deleted successfully!"
            }
    except Exception as e:
        print(f"Error deleting chat history :{e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )