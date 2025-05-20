from fastapi import APIRouter, Request, Depends
from modules.authentication.auth import auth
from modules.postings.trans import create_general_posting, retrieve_transactions, retrieve_transaction_by_id
from database.schema import ErrorResponse, PlainResponse, CreatePostingModel, TransactionModel, TransactionResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/general_posting", response_model=TransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def general_posting(request: Request, fields: CreatePostingModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_general_posting(db=db, transaction_type_id=fields.transaction_type_id, from_account_number=fields.from_account_number, to_account_number=fields.to_account_number, amount=fields.amount, narration=fields.narration)
    return req

@router.get("/", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), status: int = 0):
    filters = {}
    if status is not None:
        if  status > 0:
            filters['status'] = status
    return retrieve_transactions(db=db, filters=filters)

@router.get("/get_single/{transaction_id}", response_model=TransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), transaction_id: int = 0):
    return retrieve_transaction_by_id(db=db, transaction_id=transaction_id)
