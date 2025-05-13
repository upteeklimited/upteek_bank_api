from typing import Optional
from pydantic import BaseModel
from schemas.misc import CountryModel

class UserModel(BaseModel):
    id: int
    merchant_id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    is_new_user: Optional[bool] = None
    
    class Config:
        orm_mode = True

class ProfileModel(BaseModel):
    id: int
    user_id: int
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    mothers_maiden_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    marital_status: Optional[str] = None
    avatar: Optional[str] = None
    id_document_file: Optional[str] = None
    id_document_type: Optional[str] = None
    id_document_value: Optional[str] = None
    selfie: Optional[str] = None
    bvn: Optional[str] = None
    bvn_status: Optional[int] = 0
    nin: Optional[str] = None
    nin_status: Optional[int] = 0
    kyc_level: Optional[int] = 0
    compliance_status: Optional[int] = 0
    
    class Config:
        orm_mode = True

class SettingModel(BaseModel):
    id: int
    user_id: int
    email_notification: Optional[int] = 0
    sms_notification: Optional[int] = 0
    
    class Config:
        orm_mode = True

class MerchantModel(BaseModel):
    id: int
    user_id: int
    category_id: Optional[int] = 0
    currency_id: Optional[int] = 0
    name: Optional[str] = None
    trading_name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone_number_one: Optional[str] = None
    phone_number_two: Optional[str] = None
    opening_hours: Optional[str] = None
    closing_hours: Optional[str] = None
    logo: Optional[str] = None
    thumbnail: Optional[str] = None
    certificate: Optional[str] = None
    memorandum: Optional[str] = None
    utility_bill: Optional[str] = None
    building: Optional[str] = None
    compliance_status: Optional[int] = None
    
    class Config:
        orm_mode = True

class UserMainModel(BaseModel):
    id: int
    country_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    status: Optional[int] = 0
    created_at: Optional[str] = None
    country: Optional[CountryModel] = None
    profile: Optional[ProfileModel] = None
    merchant: Optional[MerchantModel] = None
    
    class Config:
        orm_mode = True

class AuthResponseModel(BaseModel):
    id: int
    access_token: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    profile: Optional[ProfileModel] = None
    setting: Optional[SettingModel] = None
    
    class Config:
        orm_mode = True

class MainAuthResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AuthResponseModel] = None
    
    class Config:
        orm_mode = True

class UserDetailsResponseModel(BaseModel):
    id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    profile: Optional[ProfileModel] = None
    setting: Optional[SettingModel] = None
    
    class Config:
        orm_mode = True

class UserResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserDetailsResponseModel] = None
    
    class Config:
        orm_mode = True

class UserMainResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserMainModel] = None
    
    class Config:
        orm_mode = True

class CreateUserModel(BaseModel):
    country_id: int
    username: str
    phone_number: str
    email: str
    password: str
    user_type: int = 0
    role: int = 0
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateUserModel(BaseModel):
    status: Optional[int] = 0
    role: Optional[int] = 0
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateUserPasswordModel(BaseModel):
    password: str

    class Config:
        orm_mode = True