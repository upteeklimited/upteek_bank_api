from fastapi import APIRouter, Request, Depends, HTTPException, Query
from modules.authentication.auth import auth
from modules.loans.base import get_loan_data, retrieve_loans, retrieve_single_loan
from database.schema import ErrorResponse, PlainResponse, LoanResponseModel, LoanModel, LoanDataResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)


@router.get("/data", response_model=LoanDataResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def data(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return get_loan_data(db=db)

@router.get("/get_all", response_model=Page[LoanModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), user_id: int = Query(None), merchant_id: int = Query(None), status: int = Query(None)):
    filters = {}
    if user_id:
        filters['user_id'] = user_id
    if merchant_id:
        filters['merchant_id'] = merchant_id
    if status:
        filters['status'] = status
    return retrieve_loans(db=db, filters=filters)

@router.get("/get_single/{loan_id}", response_model=LoanResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), loan_id: int = 0):
    return retrieve_single_loan(db=db, id=loan_id)
