from os.path import exists

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
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id,
        model.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user} has already voted on the post {vote.post_id}")
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vote found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
