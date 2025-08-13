from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.services.oauth2 import authenticate_client, create_access_token

router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_client(form_data.client_id, form_data.client_secret):
        raise HTTPException(
            status_code=401,
            detail="Incorrect client credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.client_id})
    return {"access_token": access_token, "token_type": "bearer"}
