from fastapi import APIRouter
from models.user_model import UserModel

router = APIRouter(prefix="/users", tags=['users'])
@router.post('register')
async def createUser(requestData: UserModel):
    return

@router.post('login')
async def login(requestData: UserModel):
    return

@router.delete('unregister/{user_id}')
async def deleteUser():
    return



