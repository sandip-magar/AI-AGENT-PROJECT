import os 
from dotenv import load_dotenv
from jose import jwt 
import bcrypt 
from fastapi import HTTPException, status 
from datetime import datetime, timezone, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))

def hash_password(plain_password: str) -> bytes: 
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password) -> bool: 
    if isinstance(hashed_password, str): 
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_new_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User doesn't credientals",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return username 
    except jwt.ExpiredSignatureError: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Token is expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    