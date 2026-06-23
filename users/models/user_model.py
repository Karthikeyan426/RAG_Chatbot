from pydantic import BaseModel

class UserModel(BaseModel):
    user_name: str
    password: str
    
class VerificationModel(BaseModel):
    access_token: str