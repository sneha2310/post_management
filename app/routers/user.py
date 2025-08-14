from .. import model, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['Users']  # This will group the endpoints under the "Posts" tag in the API documentation
)


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    user = db.query(model.User).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Users not found")
    return  user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) # status_code is used to set the response status code for create i.e. 201 instead of 200
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # read the data as Post model from the request body
    # hash the password
    user.password = utils.hash_password(user.password)
    new_user = model.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists."
        )


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return  user

