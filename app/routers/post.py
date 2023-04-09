from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import engine,get_db
from typing import Optional
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)




@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
              limit:int = 10 , skip:int = 0 , search :Optional[str]=""):
    
    """
    Returns a list of posts filtered by a search query, limited by pagination, and grouped by post ID
    """

    posts = db.query(models.Post).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts



@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
   
    """
    Creates a new post with the given data and associates it with the authenticated user
    """
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post






@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    """
    Returns a single post with the specified ID if it exists
    """
    post =db.query(models.Post).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail =f"Post with id {id} not found")
    return post


    
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    """
    Deletes the post with the specified ID, if it exists and the current user is the post owner
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if(post == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id {id} not Found!")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform this Action!")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    """
    Updates the post with the specified ID, if it exists and the current user is the post owner
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if(post == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Post with id {id} not Found!")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform this Action!")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
    
    

