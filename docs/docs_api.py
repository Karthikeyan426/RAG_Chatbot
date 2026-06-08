from fastapi import APIRouter, Depends
from sqlmodel import Session
from database_config import SessionDep
from models.doc_model import DocModel

router = APIRouter(prefix="/docs", tags=["docs"])

@router.post('/docs/upload')
async def uploadDoc(doc: DocModel, session: Session = Depends(SessionDep)):
    uploadFile = DocModel.document
    if uploadFile.content_type != "pdf":
        return "only pdf files are supported"
    