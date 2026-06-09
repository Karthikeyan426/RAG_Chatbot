from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.user_model import UserModel
from database_config import SessionDep
from database_schema import users
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=['users'])
@router.post('register', status_code = 201)
async def createUser(requestData: UserModel, session: Session = Depends(SessionDep)):
    try:
        user = users(id = requestData.user_name, password = requestData.password)
        session.add(user)
        await session.commit()
        return {"message": "user created"}
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code = 409, detail = "username already exists")


@router.post('login', status_code = 200)
async def login(requestData: UserModel, session: Session = Depends(SessionDep)):
    id = requestData.user_name
    user = await session.get(users, id)
    if not user:
        raise HTTPException(status_code = 404, detail = "user not exists")
    else:
        if user.password == requestData.password:
            return {"message": "login success"}
        else:
            raise HTTPException(status_code = 400, detail = "wrong credentials")
        

@router.delete('unregister/{user_name}', status_code = 200)
async def deleteUser(user_name: str, session: Session = Depends(SessionDep)):
    id = user_name
    user = await session.get(users, id)
    if not user:
        raise HTTPException(status_code = 404, detail = "user not exists")
    else:
        await session.delete(user)
        await session.commit()
        return {"message": "user deleted"}




