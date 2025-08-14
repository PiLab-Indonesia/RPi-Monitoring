import os
import datetime
from typing import Optional
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from .models import Database
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db = Database(settings.db_path)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_ctx.hash(password)

def create_access_token(subject: str, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = {"sub": subject}
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    with db.conn() as c:
        r = c.execute("SELECT id, username, password_hash FROM users WHERE username=?", (username,)).fetchone()
        if not r:
            return None
        if not verify_password(password, r[2]):
            return None
        return {"id": r[0], "username": r[1]}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    with db.conn() as c:
        r = c.execute("SELECT id, username FROM users WHERE username=?", (username,)).fetchone()
        if not r:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return {"id": r[0], "username": r[1]}
