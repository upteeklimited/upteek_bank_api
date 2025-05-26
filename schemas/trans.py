from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from schemas.user import UserInfoModel, MerchantModel
from schemas.misc import CountryModel, CurrencyModel
from schemas.acct import GLModel, AccountInfoModel

class TransactionTypeModel(BaseModel):
    id: int
    corresponding_gl_id: Optional[int] = None
    charge_gl_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    action: Optional[int] = None
    chargeable: Optional[int] = None
    charge_type: Optional[int] = None
    charge_percentage: Optional[float] = None
    charge_flat: Optional[float] = None
    require_approval: Optional[int] = None
    require_approval_amount: Optional[float] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CreateTransTypeModel(BaseModel):
    corresponding_gl_id: Optional[int] = 0
    charge_gl_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    action: Optional[int] = 0
    chargeable: Optional[int] = 0
    charge_type: Optional[int] = 0
    charge_percentage: Optional[float] = 0
    charge_flat: Optional[float] = 0
    require_approval: Optional[int] = 0
    require_approval_amount: Optional[float] = 0

    class Config:
        orm_mode = True

class UpdateTransTypeModel(BaseModel):
    corresponding_gl_id: Optional[int] = 0
    charge_gl_id: Optional[int] = 0
    name: Optional[str] = None
    description: Optional[str] = None
    action: Optional[int] = 0
    chargeable: Optional[int] = 0
    charge_type: Optional[int] = 0
    charge_percentage: Optional[float] = 0
    charge_flat: Optional[float] = 0
    require_approval: Optional[int] = 0
    require_approval_amount: Optional[float] = 0
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class TransTypeResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[TransactionTypeModel] = None

    class Config:
        orm_mode = True

class CreatePostingModel(BaseModel):
    transaction_type_id: int
    from_account_number: str
    to_account_number: str
    amount: float
    narration: Optional[str] = None

    class Config:
        orm_mode = True

class TransactionAccountModel(BaseModel):
    id: int
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    nuban: Optional[str] = None
    balance: Optional[float] = None
    is_gl: Optional[bool] = None

    class Config:
        orm_mode = True

class TransactionModel(BaseModel):
    id: int
    country_id: Optional[int] = 0
    currency_id: Optional[int] = 0
    user_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    gl_id: Optional[int] = 0
    account_id: Optional[int] = 0
    type_id: Optional[int] = 0
    order_id: Optional[int] = 0
    loan_id: Optional[int] = 0
    collection_id: Optional[int] = 0
    card_id: Optional[int] = 0
    institution_id: Optional[int] = 0
    bill_id: Optional[int] = 0
    beneficiary_id: Optional[int] = 0
    action: Optional[int] = 0
    reference: Optional[str] = None
    external_reference: Optional[str] = None
    description: Optional[str] = None
    narration: Optional[str] = None
    amount: Optional[float] = 0
    previous_balance: Optional[float] = 0
    new_balance: Optional[float] = 0
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    country: Optional[CountryModel] = None
    currency: Optional[CurrencyModel] = None
    user: Optional[UserInfoModel] = None
    merchant: Optional[MerchantModel] = None
    transaction_type: Optional[TransactionTypeModel] = None
    general_ledger: Optional[GLModel] = None
    account: Optional[AccountInfoModel] = None

    class Config:
        orm_mode = True

class TransactionInfoModel(BaseModel):
    id: int
    country_id: Optional[int] = 0
    currency_id: Optional[int] = 0
    user_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    type_id: Optional[int] = 0
    reference: Optional[str] = None
    external_reference: Optional[str] = None
    description: Optional[str] = None
    narration: Optional[str] = None
    amount: Optional[float] = 0
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TransactionResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[TransactionModel] = None

    class Config:
        orm_mode = True

class NewTransactionResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[TransactionInfoModel] = None

    class Config:
        orm_mode = True