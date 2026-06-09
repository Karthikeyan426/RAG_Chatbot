from pydantic import BaseModel
from  datetime import datetime
from fastapi import UploadFile

class DocModel(BaseModel):
    user_id: str
    document: UploadFile
