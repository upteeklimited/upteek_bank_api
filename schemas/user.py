from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    merchant_id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    
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

class AuthAccountModel(BaseModel):
    id: int
    user_id: int
    account_type_id: Optional[int] = 0
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    nuban: Optional[str] = None
    provider: Optional[str] = None
    available_balance: Optional[float] = 0.0
    ledger_balance: Optional[float] = 0.0
    sms_notification: Optional[int] = 0
    email_notification: Optional[int] = 0
    is_primary: Optional[int] = 0
    
    class Config:
        orm_mode = True

class AddressModel(BaseModel):
    id: int
    country_id: Optional[int] = 0
    state_id: Optional[int] = 0
    city_id: Optional[int] = 0
    lga_id: Optional[int] = 0
    addressable_type: Optional[str] = None
    addressable_id: Optional[int] = 0
    house_number: Optional[str] = None
    street: Optional[str] = None
    nearest_bus_stop: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_primary: Optional[int] = 0
    
    class Config:
        orm_mode = True

class AuthResponseModel(BaseModel):
    access_token: Optional[str] = None
    user: Optional[UserModel] = None
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
    user: Optional[UserModel] = None
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
