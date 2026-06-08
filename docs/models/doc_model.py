from pydantic import BaseModel
from  datetime import datetime
from fastapi import UploadFile

class DocModel(BaseModel):
    userid: str
    document: UploadFile
