from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from db.database import get_db
from db.models import User 
from db.schemas import UserCreate, Token, UserResponse
from core.security import hash_password, verify_password, create_new_access_token, decode_token
from sqlalchemy.orm import Session

router = APIRouter()
oauth_schema = HTTPBearer()

#router for register 
@router.post("/register-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    hashed_password = hash_password(user.password).decode('utf-8')
    new_user = User(
        username = user.username,
        hashed_password= hashed_password,
        is_active = user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/log-in", response_model=Token)
async def login_user(current_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username == current_user.username).first()
    if not users: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(current_user.password, users.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong Password or username", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not users.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenicate": "Bearer"}
        )

    access_token = create_new_access_token(data={"sub": users.username})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

#protected_route
@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth_schema), db: Session = Depends(get_db)):
    token = credentials.credentials
    username = decode_token(token)
    users = db.query(User).filter(User.username == username).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return users

#for the new_access_token
@router.post("/new-access-token", response_model=Token)
async def get_new_access_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_access_token = create_new_access_token(data={"sub": current_user.username})
    return {
        "access_token": new_access_token,
        "token_type": "Bearer"
    }