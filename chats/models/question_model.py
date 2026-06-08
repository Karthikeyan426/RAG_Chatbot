from pydantic import BaseModel

class QModel(BaseModel):
    user_id: str
    question: str
    doc_id: str