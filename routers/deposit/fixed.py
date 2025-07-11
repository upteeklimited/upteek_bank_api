from fastapi import APIRouter, Request, Depends, HTTPException, Query
from modules.authentication.auth import auth
from modules.deposits.get import retrieve_deposits, retrieve_single_deposit
# from modules.deposits.post import make_new_deposit
from database.schema import ErrorResponse, PlainResponse, DepositResponseModel, DepositModel, CreateDepositModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/deposits",
    tags=["deposits"]
)

@router.get("/", response_model=Page[DepositModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), product_id: int = Query(None, ge=0), user_id: int = Query(None, ge=0), merchant_id: int = Query(None, ge=0), gl_id: int = Query(None, ge=0), account_id: int = Query(None, ge=0), status: int = Query(None, ge=0)):
    filters = {}
    if product_id:
        filters['product_id'] = product_id
    if user_id:
        filters['user_id'] = user_id
    if merchant_id:
        filters['merchant_id'] = merchant_id
    if gl_id:
        filters['gl_id'] = gl_id
    if account_id:
        filters['account_id'] = account_id
    if status:
        filters['status'] = status
    return retrieve_deposits(db=db, filters=filters)

@router.get("/get_single/{deposit_id}", response_model=DepositResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), deposit_id: int = 0):
    return retrieve_single_deposit(db=db, deposit_id=deposit_id)
