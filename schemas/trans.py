from typing import Optional
from pydantic import BaseModel
from datetime import datetime

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