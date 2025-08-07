from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/vote',
    tags=['Vote']  # This will group the endpoints under the "Vote" tag in the API documentation
)

@router.get("/")
def get_vote():
    return {"message": "This is the vote endpoint"}

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if vote.dir == 1:
        vote_query = db.query(model.Vote).filter(
            model.Vote.post_id == vote.post_id,
            model.Vote.user_id == current_user.id
        ).first()
    return {"message": "Vote created successfully"}