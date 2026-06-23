from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from auth.current_user_extraction import get_current_user
from database_config import SessionDep
from docs.models import doc_model
from database_schema import docs, chunks
from docs.helpers import doc_embedding_coversion, doc_text_extraction
from sentence_transformers import SentenceTransformer
from config import settings

router = APIRouter(prefix="/users/user/docs", tags=["docs"])

@router.post('/upload', status_code = 201)
async def uploadDoc(session: SessionDep, currentUser: str = Depends(get_current_user), document: UploadFile = File(...)):
    uploadFile = document
    if uploadFile.content_type != "application/pdf":
        raise HTTPException(status_code = 400, detail = "file type not supported")
    else:
       doc = docs(doc_name = uploadFile.filename, user_id = currentUser)
       session.add(doc)
       session.commit()
       session.refresh(doc)


       text = doc_text_extraction.extractText(uploadFile.file)
       extracted_chunks = doc_embedding_coversion.chunk_text(text)

       model = SentenceTransformer("all-MiniLM-L6-v2", token = settings.hf_token)
       for chunk in extracted_chunks:
           converted_embedding = model.encode(chunk).tolist()
           chunk_obj = chunks(
               doc_id = doc.id,
               content = chunk,
               embedding = converted_embedding,
           )
           session.add(chunk_obj)
       session.commit()
       return {"message": "document uploaded"}

       
       

@router.delete('/{doc_id}', status_code = 200)
async def deleteDoc(doc_id: str, session: SessionDep, currentUser: str = Depends(get_current_user)):
    id = doc_id
    doc = session.get(docs, id)
    if not doc:
        raise HTTPException(status_code = 404, detail = "document not found")
    else:
        if doc.user_id != currentUser:
            raise HTTPException(status_code = 401, detail = "unauthorized document")
    session.delete(doc)
    session.commit()
    return {"message": "document deleted"}
        

@router.post(status_code = 200)
async def getUserDocs(session: SessionDep, currentUser: str = Depends(get_current_user)):
    user_id = currentUser
    docs = session.get(docs, user_id)
    if not docs:
        return {
            "docs_exists": False
        }
    else:
        return {
            "docs_exists": True,
            "docs": docs
        }

