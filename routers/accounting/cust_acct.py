from fastapi import APIRouter, Request, Depends
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
async def types_get_all(request: Request, db: Session = Depends(get_db), product_id: int = 0, name: str = None, account_code: str = None):
    filters = {}
    if product_id is not None:
        if  product_id > 0:
            filters['product_id'] = product_id
    if name is not None:
        filters['name'] = name
    if account_code is not None:
        filters['account_code'] = account_code
    return retrieve_account_types(db=db, filters=filters)

@router.get("/types/get_single/{type_id}", response_model=AccountTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def types_get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return retrieve_single_account_type(db=db, account_type_id=type_id)

@router.get("/types/get_single_by_code/{account_code}", response_model=AccountTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def types_get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_code: str = None):
    return retrieve_single_account_type_by_code(db=db, account_code=account_code)

@router.get("/", response_model=Page[AccountModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), account_type_id: int = 0, user_id: int = 0, merchant_id: int = 0, account_name: str = None, account_number: str = None, nuban: str = None, provider: str = None, manager_id: int = 0, status: int = 0):
    filters = {}
    if account_name is not None:
        filters['account_name'] = account_name
    if account_number is not None:
        filters['account_number'] = account_number
    if nuban is not None:
        filters['nuban'] = nuban
    if provider is not None:
        filters['provider'] = provider
    if status is not None:
        if  status > 0:
            filters['status'] = status
    if account_type_id is not None:
        if  account_type_id > 0:
            filters['account_type_id'] = account_type_id
    if user_id is not None:
        if  user_id > 0:
            filters['user_id'] = user_id
    if merchant_id is not None:
        if  merchant_id > 0:
            filters['merchant_id'] = merchant_id
    if manager_id is not None:
        if  manager_id > 0:
            filters['manager_id'] = manager_id
    return retrieve_accounts(db=db, filters=filters)

@router.get("/get_single/{account_id}", response_model=AccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_id: int = 0):
    return retrieve_single_account(db=db, account_id=account_id)

@router.get("/get_single_by_number/{account_number}", response_model=AccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_number: str = None):
    return retrieve_single_account_by_number(db=db, account_number=account_number)

@router.get("/virtual", response_model=Page[VirtualAccountModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def virtual_get_all(request: Request, db: Session = Depends(get_db), user_id: int = 0, financial_institution_id: int = 0, account_name: str = None, account_number: str = None, account_id: int = 0, status: int = 0, is_primary: int = 0, is_generated: int = 0):
    filters = {}
    if account_name is not None:
        filters['account_name'] = account_name
    if account_number is not None:
        filters['account_number'] = account_number
    if status is not None:
        if  status > 0:
            filters['status'] = status
    if is_primary is not None:
        if  is_primary > 0:
            filters['is_primary'] = is_primary
    if is_generated is not None:
        if  is_generated > 0:
            filters['is_generated'] = is_generated
    if user_id is not None:
        if  user_id > 0:
            filters['user_id'] = user_id
    if financial_institution_id is not None:
        if  financial_institution_id > 0:
            filters['financial_institution_id'] = financial_institution_id
    if account_id is not None:
        if  account_id > 0:
            filters['account_id'] = account_id
    return retrieve_virtual_accounts(db=db, filters=filters)

@router.get("/virtual/get_single/{virtual_account_id}", response_model=AccountResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), virtual_account_id: int = 0):
    return retrive_single_virtual_account(db=db, virtual_account_id=virtual_account_id)
