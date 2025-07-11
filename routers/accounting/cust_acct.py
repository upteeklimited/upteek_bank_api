from fastapi import APIRouter, Request, Depends, Query
from modules.authentication.auth import auth
from modules.accounting.accts import retrieve_account_types, retrieve_single_account_type, retrieve_single_account_type_by_code, retrieve_accounts, retrieve_single_account, retrieve_single_account_by_number, retrieve_virtual_accounts, retrive_single_virtual_account
from database.schema import ErrorResponse, AccountTypeModel, AccountTypeResponseModel, VirtualAccountModel, AccountModel, AccountResponseModel, VirtualAccountResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.get("/types", response_model=Page[AccountTypeModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def types_get_all(request: Request, db: Session = Depends(get_db), product_id: int = Query(None), product_type: int = Query(None), name: str = Query(None), account_code: str = Query(None)):
    filters = {}
    if product_id:
        filters['product_id'] = product_id
    if product_type:
        filters['product_type'] = product_type
    if name:
        filters['name'] = name
    if account_code:
        filters['account_code'] = account_code
    return retrieve_account_types(db=db, filters=filters)

@router.get("/types/get_single/{type_id}", response_model=AccountTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def types_get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return retrieve_single_account_type(db=db, account_type_id=type_id)

@router.get("/types/get_single_by_code/{account_code}", response_model=AccountTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def types_get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_code: str = None):
    return retrieve_single_account_type_by_code(db=db, account_code=account_code)

@router.get("/", response_model=Page[AccountModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), account_type_id: int = Query(None), product_id: int = Query(None), user_id: int = Query(None), merchant_id: int = Query(None), account_name: str = Query(None), account_number: str = Query(None), nuban: str = Query(None), provider: str = Query(None), manager_id: int = Query(None), status: int = Query(None)):
    filters = {}
    if account_name:
        filters['account_name'] = account_name
    if account_number:
        filters['account_number'] = account_number
    if nuban:
        filters['nuban'] = nuban
    if provider:
        filters['provider'] = provider
    if status:
        filters['status'] = status
    if account_type_id:
        filters['account_type_id'] = account_type_id
    if product_id:
        filters['product_id'] = product_id
    if user_id:
        filters['user_id'] = user_id
    if merchant_id:
        filters['merchant_id'] = merchant_id
    if manager_id:
        filters['manager_id'] = manager_id
    return retrieve_accounts(db=db, filters=filters)

@router.get("/get_single/{account_id}", response_model=AccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_id: int = 0):
    return retrieve_single_account(db=db, account_id=account_id)

@router.get("/get_single_by_number/{account_number}", response_model=AccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_number: str = None):
    return retrieve_single_account_by_number(db=db, account_number=account_number)

@router.get("/virtual", response_model=Page[VirtualAccountModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def virtual_get_all(request: Request, db: Session = Depends(get_db), user_id: int = Query(None), financial_institution_id: int = Query(None), account_name: str = Query(None), account_number: str = Query(None), account_id: int = Query(None), status: int = Query(None), is_primary: int = Query(None), is_generated: int = Query(None)):
    filters = {}
    if account_name:
        filters['account_name'] = account_name
    if account_number:
        filters['account_number'] = account_number
    if status:
        filters['status'] = status
    if is_primary:
        filters['is_primary'] = is_primary
    if is_generated:
        filters['is_generated'] = is_generated
    if user_id:
        filters['user_id'] = user_id
    if financial_institution_id:
        filters['financial_institution_id'] = financial_institution_id
    if account_id:
        filters['account_id'] = account_id
    return retrieve_virtual_accounts(db=db, filters=filters)

@router.get("/virtual/get_single/{virtual_account_id}", response_model=VirtualAccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), virtual_account_id: int = 0):
    return retrive_single_virtual_account(db=db, virtual_account_id=virtual_account_id)
