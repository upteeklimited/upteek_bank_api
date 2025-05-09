from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Literal

class RegisterRequest(BaseModel):
    email: str
    username: str
    phone_number: str
    password: str
    first_name: str
    other_name: Optional[str] = None
    last_name: str
    merchant_name: Optional[str] = None
    is_merchant: Optional[bool] = False
    fbt: Optional[str] = None
    
    class Config:
        orm_mode = True

class LoginEmailRequest(BaseModel):
    email: EmailStr
    password: str
    fbt: Optional[str] = None
    is_merchant: Optional[bool] = False
    
    class Config:
        orm_mode = True

class SendEmailTokenRequest(BaseModel):
    email: str
    
    class Config:
        orm_mode = True

class FinalisePasswordLessRequest(BaseModel):
    email: str
    token_str: str
    is_merchant: Optional[bool] = False
    fbt: Optional[str] = None
    
    class Config:
        orm_mode = True

class VerifyEmailTokenRequest(BaseModel):
    email: str
    token_str: str
    
    class Config:
        orm_mode = True

class CheckPhoneNumberRequest(BaseModel):
    phone_number: str
    
    class Config:
        orm_mode = True

class CheckUsernameRequest(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

class CheckEmailRequest(BaseModel):
    email: str
    
    class Config:
        orm_mode = True

class SSORequest(BaseModel):
    token: str
    provider: Literal['google', 'firebase', 'apple']
    fbt: Optional[str] = None
    is_merchant: Optional[bool] = False
    
    class Config:
        orm_mode = True