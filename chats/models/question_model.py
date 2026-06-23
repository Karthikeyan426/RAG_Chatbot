from pydantic import BaseModel

class QModel(BaseModel):
    question: str
    doc_id: str