from typing import Optional, Any, List
from pydantic import BaseModel
from datetime import datetime
from schemas.acct import AccountInfoModel

class DepositModel(BaseModel):
    id: int
    gl_id: Optional[int] = None
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    account_id: Optional[int] = None
    card_id: Optional[int] = None
    amount: Optional[float] = None
    rate: Optional[float] = None
    tenure: Optional[int] = None
    yield_amount: Optional[float] = None
    current_value: Optional[float] = None
    withholding_tax: Optional[float] = None
    VAT: Optional[float] = None
    rollover_principal: Optional[float] = None
    rollover_interest: Optional[float] = None
    rollover_at_maturity: Optional[int] = None
    liquidation_charge: Optional[float] = None
    rollover_count: Optional[int] = None
    status: Optional[int] = None  # 0 -> pending, 1 -> active, 2 -> closed, 3 -> cancelled.
    created_at: Optional[datetime] = None
    account: Optional[AccountInfoModel] = None

    class Config:
        orm_mode = True

class DepositResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[DepositModel] = None

    class Config:
        orm_mode = True

class CreateDepositModel(BaseModel):
    product_id: int
    amount: float
    rate: float
    tenure: int
    yield_amount: float
    is_account: Optional[bool] = False
    is_card: Optional[bool] = False
    card_transaction_reference: Optional[str] = None
    provider_code: Optional[str] = None

    class Config:
        orm_mode = True