from .. import schemas, models, utils, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func 


router = APIRouter(
    prefix="/posts",
    tags=["post"]
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session=Depends(get_db), 
                    current_user: int= Depends(oauth2.get_current_user),
                    limit: int =10, skip: int =0, search: Optional[str] =""):
   
    
    #posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts =db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
             models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
             models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
 
@router.get("/")
async def root():
    return {"message": "welcome to my api!"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(new_post: schemas.PostCreate, db: Session=Depends(get_db),
                        current_user: int= Depends(oauth2.get_current_user)):
  
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                   VALUES(%s, %s, %s) RETURNING *""", 
    #                (new_post.title, new_post.content, new_post.published))
    # created_post =cursor.fetchone()
    # conn.commit()
     
     new_post =models.Post(owner_id=current_user.id, **new_post.dict())
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), 
            current_user: int= Depends(oauth2.get_current_user)):
    

    post =db.query(models.Post).filter(models.Post.id == id).first()

    db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
             models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
             models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db),
                current_user: int= Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", (str(id),))
    #deleted_post =cursor.fetchone()
    #conn.commit()
    #index = find_index_post(id)
    deleted_post =db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:    
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    deleted_post.delete(synchronize_session=False)

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    #my_posts.pop(index)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db),
                current_user: int= Depends(oauth2.get_current_user)):
    
    post_query =db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return "succesfull updated"
