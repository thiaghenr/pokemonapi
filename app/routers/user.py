from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from database import get_db
from models.user import User as user_model
from schemas.user import User as user_schema, GetUser as get_user_schema
from hashing import Hash

from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/user', status_code = status.HTTP_201_CREATED, response_model = get_user_schema, tags = ['Users'])
def create_user(user: user_schema, db: Session = Depends(get_db)):
    new_user = user_model(
        name    = user.name  ,
        email  = user.email,
        password  = Hash().bcrypt(user.password)
    ) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', response_model = get_user_schema, tags = ['Users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model).filter(user_model.id == user_id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The User  with the id {user_id} was not found')
    return user