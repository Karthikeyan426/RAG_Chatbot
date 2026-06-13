from fastapi import APIRouter, HTTPException
from users.models import user_model
from database_config import SessionDep
from database_schema import users
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=['users'])
@router.post('/register', status_code = 201)
async def createUser(requestData: user_model.UserModel, session: SessionDep):
    try:
        user = users(id = requestData.user_name, password = requestData.password)
        session.add(user)
        session.commit()
        return {"message": "user created"}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code = 409, detail = "username already exists")


@router.post('/login', status_code = 200)
async def login(requestData: user_model.UserModel, session: SessionDep):
    id = requestData.user_name
    user =   session.get(users, id)
    if not user:
        raise HTTPException(status_code = 400, detail = "wrong credentials")
    else:
        if user.password == requestData.password:
            return {"message": "login success"}
        else:
            raise HTTPException(status_code = 400, detail = "wrong credentials")
        

@router.delete('/unregister/{user_name}', status_code = 200)
async def deleteUser(user_name: str, session: SessionDep):
    id = user_name
    user = session.get(users, id)
    if not user:
        raise HTTPException(status_code = 404, detail = "user not exists")
    else:
        session.delete(user)
        session.commit()
        return {"message": "user deleted"}




