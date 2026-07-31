from datetime import datetime
from uuid import UUID
from .enums import UserType

from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  
    user_type: UserType
    company_name: str
    
class UserCreate(UserBase):
    password_hash: str

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password_hash: str | None = None
    user_type: UserType| None = None
    company_name: str | None = None
      
class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: UUID
    created_at: datetime
