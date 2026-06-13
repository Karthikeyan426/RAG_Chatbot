from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from database_config import SessionDep
from docs.models import doc_model
from database_schema import docs, chunks
from docs.helpers import doc_embedding_coversion, doc_text_extraction
from sentence_transformers import SentenceTransformer

router = APIRouter(prefix="/users/user/docs", tags=["docs"])

@router.post('/upload', status_code = 201)
async def uploadDoc(session: SessionDep, user_id: str = Form(...), document: UploadFile = File(...)):
    uploadFile = document
    if uploadFile.content_type != "application/pdf":
        raise HTTPException(status_code = 400, detail = "file type not supported")
    else:
       doc = docs(doc_name = uploadFile.filename, user_id = user_id)
       session.add(doc)
       session.commit()
       session.refresh(doc)


       text = doc_text_extraction.extractText(uploadFile.file)
       extracted_chunks = doc_embedding_coversion.chunk_text(text)

       model = SentenceTransformer("all-MiniLM-L6-v2")
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
async def deleteDoc(doc_id: str, session: SessionDep):
    id = doc_id
    doc = session.get(docs, id)
    session.delete(doc)
    session.commit()
    return {"message": "document deleted"}
        
    