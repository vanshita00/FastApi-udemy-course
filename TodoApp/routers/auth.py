from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlmodel import Session
from models import Users
from database import engine,SessionLocal
from jose import JWTError, jwt
from fastapi import status

router=APIRouter(
    tags=['auth']

)

SECRET_KEY='53eee1950605f91c0a7cf60bace4739d801b0780539136bac06805fd87ae0517'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='token')



class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

def authentication_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,role:str):

    encode={'sub':username,'id':user_id,'role':role}   
    # expires=datetime.utcnow()+expires_delta
    # encode.update({'exp':expires})
    jwtToken = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    # print(jwtToken)
    return jwtToken

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)] ):
    try:
        print(oauth2_bearer)
        payload=jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        user_role:str=payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not a validate user.')
        
        return {'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
        print(JWTError)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the user.')

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,
    create_user_request:CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()
    return create_user_request
    

@router.post("/token")
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:db_dependency):
    user=authentication_user(form_data.username,form_data.password,db)
    if not user:
        return 'Failed Authentication'

    token=create_access_token(user.username,user.id,user.role)
    return {'access_token':token,'token_type':'bearer'}


