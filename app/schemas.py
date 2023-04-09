from pydantic import BaseModel,EmailStr, conint,Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):

    """
    Base schema for a Post object.
    """
    title: str
    content: str
    published:bool = True


class PostCreate(PostBase):
    """
    Schema for creating a new Post object.
    Inherits from PostBase.
    """
    pass


class UserCreate(BaseModel):

    """
    Schema for creating a new User object.
    """
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):

    """
    Schema for returning a User object.
    """
    id:int
    email: EmailStr
    created_at:datetime
    class Config:
        orm_mode = True
    

class UserLogin(BaseModel):

    """
    Schema for authenticating a User object.
    """
    email:EmailStr
    password:str
    
    
class Post(PostBase):

    """
    Schema for a Post object.
    Inherits from PostBase.
    """
    id:int
    created_at:datetime
    owner_id:int
    owner : UserOut
    
    class Config:
        orm_mode = True
        
        
class PostOut(BaseModel):
    """
    Schema for returning a Post object.
    """
    Post: Post 
    class Config:
        orm_mode = True
    
    
    
    
    
class Token(BaseModel):
    
    """
    Schema for a JWT token.
    """
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    
    """
    Schema for data stored in a JWT token.
    """
    id:Optional[str]=None
    
 
