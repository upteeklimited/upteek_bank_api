from typing import Optional, Any, Dict, List, Literal
from pydantic import BaseModel
from datetime import datetime

class OrderedProductModel(BaseModel):
    product_id: int
    quantity: int
    amount: float
    
    class Config:
        orm_mode = True

class CreateOrderRequest(BaseModel):
    address_id: Optional[int] = 0
    is_account: Optional[bool] = False
    is_card: Optional[bool] = False
    card_id: Optional[int] = 0
    card_transaction_reference: Optional[str] = None
    save_card: Optional[bool] = False
    provider_code: Optional[Literal['paystack', 'flutterwave']] = None
    products: List[OrderedProductModel] = None
    amount: float
    total_amount: float
    discount: Optional[float] = 0.0
    
    class Config:
        orm_mode = True

class OrderProductsModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    amount: float
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class OrderMainModel(BaseModel):
    id: int
    merchant_id: Optional[int] = 0
    reference: Optional[str] = None
    sub_total: float
    total_amount: float
    discount: Optional[float] = 0.0
    address_id: Optional[int] = 0
    status: Optional[int] = 0
    order_products: List[OrderProductsModel] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class OrderModel(BaseModel):
    id: int
    user_id: Optional[int] = 0
    merchant_id: Optional[int] = 0
    currency_id: Optional[int] = 0
    reference: Optional[str] = None
    sub_total: float
    total_amount: float
    discount: Optional[float] = 0.0
    address_id: Optional[int] = 0
    payment_status: Optional[int] = 0
    delivery_status: Optional[int] = 0
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class NewOrderResponse(BaseModel):
    status: bool
    message: str
    data: Optional[OrderMainModel] = None

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    status: bool
    message: str
    data: Optional[OrderModel] = None

    class Config:
        orm_mode = True