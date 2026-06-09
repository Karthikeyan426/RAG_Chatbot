from fastapi import APIRouter, Depends
from sqlmodel import Session
from database_config import SessionDep
from models.question_model import QModel
from database_schema import chats
from sentence_transformers import SentenceTransformer
from sqlmodel import text
from config import settings
from groq import Groq

router = APIRouter(prefix='/users/user/chats', tags=['chats'])

@router.post('/enquery', status_code = 200)
async def processEnquery(requestData: QModel, session: Session = Depends(SessionDep)):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    qEmbedding = model.encode(requestData.question).tolist()
    similarQ = session.exec(
        text("""
            SELECT response_content
            FROM chats
            WHERE 1 - (embedding <=> :question_embedding::vector) > 0.90
            ORDER BY embedding <=> :question_embedding::vector
            LIMIT 1
        """),
        {"embedding": str(qEmbedding)}
    ).first()

    if similarQ:
        chat = chats(
            doc_id= requestData.doc_id,
            question_content = requestData.question,
            user_id = requestData.user_id,
            response_content = similarQ.response_content
        )
        session.add(chat)
        await session.commit()
        return {"response": similarQ.response_content}
    else:
        similarChunks = session.exec(
        text("""
            SELECT content, 1 - (embedding <=> :embedding::vector) AS similarity
            FROM chunks
            ORDER BY embedding <=> :embedding::vector
            LIMIT :limit
        """),
        {"embedding": str(qEmbedding), "limit": 5}
        )

        context = "\n".join([chunk.content for chunk in similarChunks])
        client = Groq(api_key = settings.groq_api_key)
        response = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = [
                {
                    "role": "system",
                    "content": f"Answer the question based on this context:\n{context}"
                },
                {
                    "role": "user",
                    "content": requestData.question
                }
            ]
        )

        receivedResponse = response.choices[0].message.content
        chat = chats(
            doc_id = requestData.doc_id,
            user_id = requestData.user_id,
            question_content = requestData.question,
            question_embedding = qEmbedding,
            response_content = receivedResponse
        )
        session.add(chat)
        await session.commit()

        return {"response": receivedResponse}




    

@router.delete('/{chat_id}',status_code = 200)
async def deleteChat(chat_id: str, session: Session = Depends(SessionDep)):
    id = chat_id
    chat = await session.get(chats, id)
    await session.delete(chat)
    await  session.commit()
    return {"message": "chat deleted", "id": id}



@router.get('/{chat_id}', status_code = 200)
async def getChat(chat_id: str, session: Session = Depends(SessionDep)):
    id = chat_id
    chat = await session.get(chats, id)
    return {"chat_q": chat.question_content, "chat_a": chat.response_content}