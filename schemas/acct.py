from typing import Optional, List, Any
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from schemas.user import UserInfoModel, MerchantModel

class GLTypeModel(BaseModel):
    id: int
    country_id: Optional[int] = None
    currency_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    account_code: Optional[str] = None
    type_number: Optional[int] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CreateGLTypeModel(BaseModel):
    name: str
    description: Optional[str] = None
    type_number: int = Field(..., ge=1, le=4, description="Must be between 1 and 4")

    class Config:
        orm_mode = True

class UpdateGLTypeModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GLTypeResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[GLTypeModel] = None

    class Config:
        orm_mode = True

class GLModel(BaseModel):
    id: int
    type_id: int
    parent_id: Optional[int] = 0
    name: str
    account_number: str
    description: Optional[str] = None
    balance: Optional[float] = 0
    status: Optional[int] = 0
    created_at: Optional[datetime] = None
    gl_type: Optional[GLTypeModel] = None

    class Config:
        orm_mode = True

class CreateGLModel(BaseModel):
    type_id: int
    parent_id: Optional[int] = 0
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class UpdateGLModel(BaseModel):
    description: Optional[str] = None
    status: Optional[int] = None
    manager_id: Optional[int] = None

    class Config:
        orm_mode = True

class GLResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[GLModel] = None

    class Config:
        orm_mode = True

class AccountTypeModel(BaseModel):
    id: int
    product_id: int
    name: str
    description: Optional[str] = None
    account_code: str
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class AccountTypeResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AccountTypeModel] = None

    class Config:
        orm_mode = True

class FinancialProductModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    product_type: int
    user_type: int
    individual_compliance_type: Optional[int] = None
    merchant_compliance_type: Optional[int] = None
    interest_rate: Optional[float] = None
    overdrawn_interest_rate: Optional[float] = None
    charge_if_overdrawn: Optional[float] = None
    charges: Optional[float] = None
    cot_rate: Optional[float] = None
    minimum_amount: Optional[float] = None
    maximum_amount: Optional[float] = None
    liquidation_penalty: Optional[float] = None
    tenure: Optional[int] = None
    interest_tenure_type: Optional[int] = None
    interest_tenure_data: Optional[Any] = None
    guarantor_requirement: Optional[int] = None
    amount_to_require_guarantor: Optional[float] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None
    account_type: Optional[AccountTypeModel] = None

    class Config:
        orm_mode = True

class FinancialProductMiniModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    product_type: int
    user_type: int
    individual_compliance_type: Optional[int] = None
    merchant_compliance_type: Optional[int] = None
    overdrawn_interest_rate: Optional[float] = None
    charge_if_overdrawn: Optional[float] = None
    charges: Optional[float] = None
    cot_rate: Optional[float] = None
    minimum_amount: Optional[float] = None
    maximum_amount: Optional[float] = None
    liquidation_penalty: Optional[float] = None
    tenure: Optional[int] = None
    interest_tenure_type: Optional[int] = None
    interest_tenure_data: Optional[str] = None
    guarantor_requirement: Optional[int] = None
    amount_to_require_guarantor: Optional[float] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CreateFinancialProductModel(BaseModel):
    name: str
    description: Optional[str] = None
    product_type: int
    user_type: int
    individual_compliance_type: Optional[int] = None
    merchant_compliance_type: Optional[int] = None
    interest_rate: Optional[float] = None
    overdrawn_interest_rate: Optional[float] = None
    charge_if_overdrawn: Optional[float] = None
    charges: Optional[float] = None
    cot_rate: Optional[float] = None
    minimum_amount: Optional[float] = None
    maximum_amount: Optional[float] = None
    liquidation_penalty: Optional[float] = None
    tenure: Optional[int] = None
    interest_tenure_type: Optional[int] = None
    interest_tenure_data: Optional[Any] = None
    guarantor_requirement: Optional[int] = None
    amount_to_require_guarantor: Optional[float] = None
    instant_interest_pay_status: Optional[int] = None

    @model_validator(mode='after')
    def check_min_max(self):
        if self.minimum_amount is not None and self.maximum_amount is not None:
            if self.minimum_amount > self.maximum_amount:
                raise ValueError('minimum_amount cannot be greater than maximum_amount')
        return self

    class Config:
        orm_mode = True

class UpdateFinancialProductModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    product_type: Optional[int] = None
    user_type: Optional[int] = None
    individual_compliance_type: Optional[int] = None
    merchant_compliance_type: Optional[int] = None
    interest_rate: Optional[float] = None
    overdrawn_interest_rate: Optional[float] = None
    charge_if_overdrawn: Optional[float] = None
    charges: Optional[float] = None
    cot_rate: Optional[float] = None
    minimum_amount: Optional[float] = None
    maximum_amount: Optional[float] = None
    liquidation_penalty: Optional[float] = None
    tenure: Optional[int] = None
    interest_tenure_type: Optional[int] = None
    interest_tenure_data: Optional[Any] = None
    guarantor_requirement: Optional[int] = None
    amount_to_require_guarantor: Optional[float] = None
    status: Optional[int] = None

    @model_validator(mode='after')
    def check_min_max(self):
        if self.minimum_amount is not None and self.maximum_amount is not None:
            if self.minimum_amount > self.maximum_amount:
                raise ValueError('minimum_amount cannot be greater than maximum_amount')
        return self

    class Config:
        orm_mode = True

class FinancialProductResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[FinancialProductModel] = None

    class Config:
        orm_mode = True

class VirtualAccountModel(BaseModel):
    id: int
    user_id: Optional[int] = 0
    account_id: Optional[int] = 0
    financial_institution_id: Optional[int] = 0
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    is_primary: Optional[int] = 0
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class AccountModel(BaseModel):
    id: int
    account_type_id: Optional[int] = 0
    user_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    nuban: Optional[str] = None
    provider: Optional[str] = None
    available_balance: Optional[float] = 0
    ledger_balance: Optional[float] = 0
    sms_notification: Optional[int] = 0
    email_notification: Optional[int] = 0
    is_primary: Optional[int] = 0
    manager_id: Optional[int] = 0
    last_active_at: Optional[datetime] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None
    account_type: Optional[AccountTypeModel] = None
    user: Optional[UserInfoModel] = None
    merchant: Optional[MerchantModel] = None
    virtual_accounts: Optional[List[VirtualAccountModel]] = None

    class Config:
        orm_mode = True

class AccountInfoModel(BaseModel):
    id: int
    account_type_id: Optional[int] = 0
    user_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    nuban: Optional[str] = None
    provider: Optional[str] = None
    available_balance: Optional[float] = 0
    ledger_balance: Optional[float] = 0
    sms_notification: Optional[int] = 0
    email_notification: Optional[int] = 0
    is_primary: Optional[int] = 0
    manager_id: Optional[int] = 0
    last_active_at: Optional[datetime] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None
    account_type: Optional[AccountTypeModel] = None

    class Config:
        orm_mode = True

class AccountResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AccountModel] = None

    class Config:
        orm_mode = True

class VirtualAccountResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[VirtualAccountModel] = None

    class Config:
        orm_mode = True