from fastapi import APIRouter, Depends
from sqlmodel import Session
from models.user_model import UserModel
from database_config import SessionDep

router = APIRouter(prefix="/users", tags=['users'])
@router.post('register')
async def createUser(requestData: UserModel, session: Session = Depends(SessionDep)):
    return

@router.post('login')
async def login(requestData: UserModel, session: Session = Depends(SessionDep)):
    return

@router.delete('unregister/{user_id}')
async def deleteUser(session: Session = Depends(SessionDep)):
    return



