from sqlalchemy import func
from app import oauth2
from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy.exc import IntegrityError



router = APIRouter(
    prefix= "/users",
    tags=['Users']
)


@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user:schemas.UserCreate,db:Session=Depends(get_db)):
    
    """
    Creates a new user with the given email and password, and returns the user information.
    """
    hashed_password = utils.hash(user.password)
    mail = user.email
    try:
        new_user=models.User(email=mail,password=hashed_password,role="guest")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=403,
            detail='This email is already in use'
        )
    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):

    """
    Fetches user information for the user with the specified ID, if it exists
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail =f"User with id {id} not found")
    
    return user

@router.get("/",response_model=List[schemas.UserOut])
def get_users(db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    """
    Returns a list of all users in the database, only if the current user is an admin.
    """
    login= db.query(models.User).filter(models.User.id==current_user.id).first()
    role = login.role
    if(role!="admin"):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform this Action!")

    users = db.query(models.User).all()
    return  users
    


@router.put("/{id}",response_model=schemas.UserOut)
def update_user(id:int,updated_user:schemas.UserCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    """
    Update a user with the specified ID, if it exists and the current user is the same user being updated.

    """
    
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first() 
    if(user == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {id} not Found!")
    if user.id!=current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform this Action!")
    hashed_password = utils.hash(updated_user.password)
    updated_user.password = hashed_password
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first()


@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    """
    Deletes the user with the specified ID, if it exists and the current user is an admin
    """

    login= db.query(models.User).filter(models.User.id==current_user.id).first()
    role = login.role
    if(role!="admin"):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Not Authorized to perform this Action!")

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if(user == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {id} not Found!")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)