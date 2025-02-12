from pydantic import BaseModel
import uuid
from typing import Optional
from beanie import Document
from pydantic import Field
from beanie import PydanticObjectId as ObjectId

class ImageDocument(Document):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    description: str
    ztf_id: str
    user: str


    class Settings:
        collection = "images"

class reaction(Document):

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    ztf_id: str
    tag: str
    user: Optional[str] = None
    changed_at: Optional[str] = None
    
    class Config:
        scheme_extra = {
            "example": {
            'ztf_id': 'ZTF18aazmwmw',
            'tag': 'Anomaly',
            'user': 'Anastasia',
            'changed_at': '22.11.2023 17:50'
            }
        }
    
    class Settings:
        name = "reactions_"


class update_reaction(BaseModel):
    id: Optional[str]
    tag: Optional[str]
    user: Optional[str]
    changed_at: Optional[str]
    
    class Config:
        scheme_extra = {
            "example": {
            'id': 'ZTF18aazmwmw',
            'tag': 'Anomaly',
            'user': 'Anastasia',
            'changed_at': '22.11.2023 17:50'
            }
        }
        
class User(Document):
    name: str
    password: str
    tg_id: Optional[str] = 'ND'
    full_name: Optional[str]= ''
    
    class Settings:
        name = "users"
    
    class Config:
        scheme_extra = {
            "example": {
            'name': 'Anastasia',
            'password': '0000',
            'tg_id': '5365634',
            'full_name': 'Anastasia Baluta'
            }
        }
        

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
