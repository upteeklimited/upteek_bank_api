from typing import Optional
from fastapi import Form
from pydantic import BaseModel

class UpdateBasicProfileRequestModel(BaseModel):
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    merchant_category_id: Optional[int] = None
    merchant_currency_id: Optional[int] = None
    merchant_name: Optional[str] = None
    merchant_trading_name: Optional[str] = None
    merchant_description: Optional[str] = None
    merchant_email: Optional[str] = None
    merchant_phone_number: Optional[str] = None
    
    class Config:
        orm_mode = True

def parse_update_basic_profile_payload(fields: str = Form(...)) -> UpdateBasicProfileRequestModel:
    return UpdateBasicProfileRequestModel.model_validate_json(fields)

class UpdatePasswordRequestModel(BaseModel):
    password: str
    old_password: str
    
    class Config:
        orm_mode = True

class UpdateSettingsRequestModel(BaseModel):
    email_notification: Optional[int] = None
    sms_notification: Optional[int] = None
    dashboard_state: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateAddressRequestModel(BaseModel):
    state_id: Optional[int] = None
    city_id: Optional[int] = None
    lga_id: Optional[int] = None
    house_number: Optional[str] = None
    street: Optional[str] = None
    nearest_bus_stop: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    
    class Config:
        orm_mode = True

class SmileIDPayloadRequestModel(BaseModel):
    job_id: str
    
    class Config:
        orm_mode = True

class SmileIDGenerateWebTokenRequestModel(BaseModel):
    product: str
    callback_url: str
    
    class Config:
        orm_mode = True

class SmileIDWebTokenModel(BaseModel):
    token: str
    job_id: str
    
    class Config:
        orm_mode = True

class SmileIDWebTokenResponse(BaseModel):
    status: bool
    message: str
    data: Optional[SmileIDWebTokenModel] = None
    
    class Config:
        orm_mode = True

class SmileIDComplainceFinaliseModel(BaseModel):
    card_back_url: str
    card_image_url: str
    selfie_image_url: str
    
    class Config:
        orm_mode = True

class SmileIDComplainceFinaliseResponse(BaseModel):
    status: bool
    message: str
    data: Optional[SmileIDComplainceFinaliseModel] = None
    
    class Config:
        orm_mode = True

class SmileIDMerchantComplainceFinaliseModel(BaseModel):
    certificate_url: str
    
    class Config:
        orm_mode = True

class SmileIDMerchantComplainceFinaliseResponse(BaseModel):
    status: bool
    message: str
    data: Optional[SmileIDMerchantComplainceFinaliseModel] = None
    
    class Config:
        orm_mode = True