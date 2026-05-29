from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from passlib.context import CryptContext


from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


session = Session(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw: str):
    password = pw[:72]
    return pwd_context.hash(password)

def verify_password(pw, hashed_pw):
    return pwd_context.verify(pw, hashed_pw)


#CREATE JWT TOKEN
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_TOKEN = 60

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TOKEN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token tidak valid!"
        )
    
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user_id = int(payload.get("sub"))
    user = session.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="user tidak ditemukan"
            )
    return user
