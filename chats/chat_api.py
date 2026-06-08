from fastapi import APIRouter
from models.question_model import QModel

router = APIRouter(prefix='/users/user/chats', tags=['chats'])

@router.post('/enquery')
async def processEnquery(requestData: QModel):
    return

@router.delete('/{chat_id}')
async def deleteChat():
    return

@router.get('/{chat_id}')
async def getChat():
    return