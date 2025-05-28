from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class DashboardDataModel(BaseModel):
    customers_count: Optional[int] = 0
    merchants_count: Optional[int] = 0
    customers_and_merchants_count: Optional[int] = 0
    total_deposits: Optional[float] = 0
    total_deposits_count: Optional[int] = 0
    active_loans: Optional[float] = 0
    total_accounts: Optional[int] = 0

    class Config:
        orm_mode = True

class DashboardDataResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[DashboardDataModel] = None

    class Config:
        orm_mode = True