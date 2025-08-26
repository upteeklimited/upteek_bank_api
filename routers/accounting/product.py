from fastapi import APIRouter, Request, Depends, Query
from modules.authentication.auth import auth
from modules.accounting.prods import create_new_financial_product, update_existing_financial_product, delete_existing_financial_product, retrieve_financial_products, retrieve_single_financial_product
from database.schema import ErrorResponse, PlainResponse, FinancialProductModel, CreateFinancialProductModel, UpdateFinancialProductModel, FinancialProductResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/financial_products",
    tags=["financial_products"]
)

@router.post("/create", response_model=FinancialProductResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateFinancialProductModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_new_financial_product(db=db, name=fields.name, description=fields.description, product_type=fields.product_type, user_type=fields.user_type, individual_compliance_type=fields.individual_compliance_type, merchant_compliance_type=fields.merchant_compliance_type, interest_rate=fields.interest_rate, overdrawn_interest_rate=fields.overdrawn_interest_rate, charge_if_overdrawn=fields.charge_if_overdrawn, charges=fields.charges, cot_rate=fields.cot_rate, minimum_amount=fields.minimum_amount, maximum_amount=fields.maximum_amount, liquidation_penalty=fields.liquidation_penalty, tenure=fields.tenure, interest_tenure_type=fields.interest_tenure_type, interest_tenure_data=fields.interest_tenure_data, guarantor_requirement=fields.guarantor_requirement, amount_to_require_guarantor=fields.amount_to_require_guarantor, instant_interest_pay_status=fields.instant_interest_pay_status, created_by=user['id'])
    return req

@router.post("/update/{product_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateFinancialProductModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), product_id: int=0):
    values = fields.model_dump()
    req = update_existing_financial_product(db=db, product_id=product_id, values=values)
    return req

@router.get("/delete/{product_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), product_id: int = 0):
    return delete_existing_financial_product(db=db, product_id=product_id)

@router.get("/", response_model=Page[FinancialProductModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), name: str = Query(None), status: int = Query(None), country_id: int = Query(None), currency_id: int = Query(None), product_type: int = Query(None), user_type: int = Query(None), individual_compliance_type: int = Query(None), merchant_compliance_type: int = Query(None)):
    filters = {}
    if name:
        filters['name'] = name
    if status:
        filters['status'] = status
    if country_id:
        filters['country_id'] = country_id
    if currency_id:
        filters['currency_id'] = currency_id
    if product_type:
        filters['product_type'] = product_type
    if user_type:
        filters['user_type'] = user_type
    if individual_compliance_type:
        filters['individual_compliance_type'] = individual_compliance_type
    if merchant_compliance_type:
        filters['merchant_compliance_type'] = merchant_compliance_type
    return retrieve_financial_products(db=db, filters=filters)

@router.get("/get_single/{product_id}", response_model=FinancialProductResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), product_id: int = 0):
    return retrieve_single_financial_product(db=db, product_id=product_id)
