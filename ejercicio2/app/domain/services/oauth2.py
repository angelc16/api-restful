import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.domain.models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "demo-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
CLIENT_ID_TEST = os.getenv("CLIENT_ID_TEST", "test_client")
CLIENT_SECRET_TEST = os.getenv("CLIENT_SECRET_TEST", "test_secret")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_client(client_id: str, client_secret: str) -> bool:
    print(f"Authenticating client_id: {client_id} with client_secret: {client_secret}")
    if client_id == CLIENT_ID_TEST and client_secret == CLIENT_SECRET_TEST:
        return True
    return False


def create_access_token(data: dict) -> str:
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + (delta)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        return User(id=1, client_id=client_id)
    except JWTError:
        raise credentials_exception
