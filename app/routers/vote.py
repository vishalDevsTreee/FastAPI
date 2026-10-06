from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix ="/vote",
    tags =['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session =Depends(get_db),
         current_user: int =Depends(oauth2.get_current_user)):

    post =db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} does not exist")

    vote_query =db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                             models.Vote.user_id == current_user.id).first()

    if vote.dir == 1:
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on the post {vote.post_id}")
        new_vote =models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exists")
        db.delete(vote_query)
        db.commit()
        return {"message": "successfully deleted vote"}
    
            
    
