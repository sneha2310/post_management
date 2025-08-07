from os import access

from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, model, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #  user_credentials = {"username": "test", "password": "password"} it returns this dict
    user = db.query(model.User).filter(
        model.User.email == user_credentials.username  # OAuth2PasswordRequestForm uses 'username' for email
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
