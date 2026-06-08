from fastapi import APIRouter
from models.doc_model import DocModel

router = APIRouter(prefix="/docs", tags=["docs"])

@router.post('/docs/upload')
async def uploadDoc(doc: DocModel):
    uploadFile = DocModel.document
    if uploadFile.content_type != "pdf":
        return "only pdf files are supported"
    