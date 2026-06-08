from fastapi import APIRouter, Depends
from sqlmodel import Session
from database_config import SessionDep
from models.question_model import QModel

router = APIRouter(prefix='/users/user/chats', tags=['chats'])

@router.post('/enquery')
async def processEnquery(requestData: QModel, session: Session = Depends(SessionDep)):
    return

@router.delete('/{chat_id}')
async def deleteChat(session: Session = Depends(SessionDep)):
    return

@router.get('/{chat_id}')
async def getChat(session: Session = Depends(SessionDep)):
    return