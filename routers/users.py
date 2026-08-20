from fastapi import APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session 
from db.database import get_db
from db.models import User
from db.schemas import UserResponse, UserUpdate
from core.security import hash_password
from typing import List
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_all_user(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).offset(skip).limit(limit).all()
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, current_user: User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user 

@router.put("/{user_id}")
async def update_user(user_id:int, updated_user: UserUpdate, current_usera: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if updated_user.username is not None:
        user.username = updated_user.username
    if updated_user.password is not None:
        user.hashed_password = hash_password(updated_user.hashed_password)

    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}")
async def delete_user(user_id:int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    db.delete(user)
    db.commit()

    return {"message": "User deleted sucessfull!"}
        