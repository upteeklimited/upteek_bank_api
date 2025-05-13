from typing import Optional, Any, Dict, List
from pydantic import BaseModel
from datetime import datetime
from schemas.misc import CurrencyModel
from schemas.user import MerchantModel

class CreateCategoryRequest(BaseModel):
    category_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateCategoryRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class CategoryModel(BaseModel):
    id: int
    category_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CategoryResponse(BaseModel):
    status: bool
    message: str
    data: Optional[CategoryModel] = None

    class Config:
        orm_mode = True

class CreateGroupRequest(BaseModel):
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateGroupRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GroupModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class GroupResponse(BaseModel):
    status: bool
    message: str
    data: Optional[GroupModel] = None

    class Config:
        orm_mode = True

class TagModel(BaseModel):
    id: int
    merchant_id: Optional[int] = 0
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ProductFileMetaData(BaseModel):
    filename: Optional[str] = None
    url: Optional[str] = None
    external_reference: Optional[str] = None

    class Config:
        orm_mode = True

class VariantModel(BaseModel):
    id: int
    product_id: Optional[int] = 0
    attributes: Optional[str] = None
    amount: Optional[float] = 0
    files_meta_data: Optional[List[ProductFileMetaData]] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ProductModel(BaseModel):
    id: int
    merchant_id: Optional[int] = 0
    category_id: Optional[int] = 0
    currency_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    slug: Optional[str] = None
    product_type: Optional[int] = 0
    units: Optional[int] = 0
    weight: Optional[float] = 0
    cost_price: Optional[float] = 0
    price: Optional[float] = 0
    discount_price: Optional[float] = 0
    discount: Optional[float] = 0
    discount_type: Optional[int] = 0
    special_note: Optional[str] = None
    unit_low_level: Optional[int] = 0
    files_meta_data: Optional[List[ProductFileMetaData]] = None
    condition_status: Optional[int] = 0
    status: Optional[int] = 0
    created_at: Optional[datetime] = None
    category: Optional[CategoryModel] = None
    categories: Optional[List[CategoryModel]] = None
    groups: Optional[List[CategoryModel]] = None
    currency: Optional[CurrencyModel] = None
    tags: Optional[List[TagModel]] = None
    merchant: Optional[MerchantModel] = None
    # variants: Optional[List[VariantModel]] = None

    class Config:
        orm_mode = True

class ProductFieldModel(BaseModel):
    category_id: Optional[int] = None
    currency_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    product_type: Optional[int] = None
    units: Optional[int] = None
    weight: Optional[int] = None
    cost_price: Optional[float] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    discount: Optional[float] = None
    discount_type: Optional[int] = None
    special_note: Optional[str] = None
    unit_low_level: Optional[int] = None
    status: Optional[int] = None
    notify_if_available: Optional[int] = None
    condition_status: Optional[int] = None

    class Config:
        orm_mode = True

class UpdateMultiProductRequest(BaseModel):
    product_ids: List[int]
    values: Optional[ProductFieldModel]

    class Config:
        orm_mode = True

class UpdateDiverseProductRequest(BaseModel):
    product_id: int
    category_id: Optional[int] = None
    currency_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    product_type: Optional[int] = None
    units: Optional[int] = None
    weight: Optional[int] = None
    cost_price: Optional[float] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    discount: Optional[float] = None
    discount_type: Optional[int] = None
    special_note: Optional[str] = None
    unit_low_level: Optional[int] = None
    status: Optional[int] = None
    notify_if_available: Optional[int] = None
    condition_status: Optional[int] = None

    class Config:
        orm_mode = True


class ProductResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[ProductModel] = None

    class Config:
        orm_mode = True

class MiniProductModel(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    cost_price: Optional[float] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    units: Optional[int] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class MiniProductResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[List[MiniProductModel]] = None

    class Config:
        orm_mode = True
