from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database_config import SessionDep
from models.doc_model import DocModel
from database_schema import docs, chunks
from helpers import doc_embedding_coversion, doc_text_extraction
from sentence_transformers import SentenceTransformer

router = APIRouter(prefix="/docs", tags=["docs"])

@router.post('/upload', status_code = 201)
async def uploadDoc(doc: DocModel, session: Session = Depends(SessionDep)):
    uploadFile = doc.document
    if uploadFile.content_type != "application/pdf":
        raise HTTPException(status_code = 400, detail = "file type not supported")
    else:
       doc = docs(doc_name = uploadFile.filename, user_id = doc.user_id)
       session.add(doc)
       await session.commit()
       await session.refresh(doc)


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
async def deleteDoc(doc_id: str, session: Session = Depends(SessionDep)):
    id = doc_id
    doc = await session.get(docs, id)
    await session.delete(doc)
    await session.commit()
    return {"message": "document deleted"}
        
    