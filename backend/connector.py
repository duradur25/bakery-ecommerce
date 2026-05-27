from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from passlib.context import CryptContext

engine = create_engine("mysql+pymysql://root:secret@localhost:3306/test")

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
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_TOKEN = 60

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TOKEN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




