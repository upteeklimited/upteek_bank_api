from fastapi import APIRouter, Request, Depends, HTTPException, Query
from modules.authentication.auth import auth
from modules.loans.applications import retrieve_loan_applications, retrieve_single_loan_application, do_entry_level_application_approval, do_entry_level_application_rejection, do_authorizer_loan_application_rejection, do_authorizer_loan_application_approval
from database.schema import ErrorResponse, PlainResponse, LoanApplicationModel, LoanApplicationResponseModel, LoanResponseModel, LoanApplicationApprovalModel, LoanApplicationDeclineModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page
from settings.constants import USER_TYPES

router = APIRouter(
    prefix="/loan_applications",
    tags=["loan_applications"]
)


@router.get("/get_all", response_model=Page[LoanApplicationModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), user_id: int = Query(None), merchant_id: int = Query(None), approval_level: int = Query(None), status: int = Query(None), top_up_status: int = Query(None)):
    filters = {}
    if user_id:
        filters['user_id'] = user_id
    if merchant_id:
        filters['merchant_id'] = merchant_id
    if approval_level:
        filters['approval_level'] = approval_level
    if status:
        filters['status'] = status
    if top_up_status:
        filters['top_up_status'] = top_up_status
    return retrieve_loan_applications(db=db, filters=filters)

@router.get("/get_single/{loan_application_id}", response_model=LoanApplicationResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), loan_application_id: int = 0):
    return retrieve_single_loan_application(db=db, id=loan_application_id)

@router.post("/entry_level/approve", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def entry_level_approve(request: Request, fields: LoanApplicationApprovalModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    if user['role'] != USER_TYPES['bank']['roles']['clerk']['num']:
        raise HTTPException(status_code=403, detail={'status': False, 'message': 'You are not authorized to perform this action'})
    req = do_entry_level_application_approval(db=db, user_id=user['id'], loan_application_id=fields.loan_application_id)
    if req['status'] == False:
        raise HTTPException(status_code=400, detail=req)
    return req

@router.post("/entry_level/reject", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def entry_level_reject(request: Request, fields: LoanApplicationDeclineModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    if user['role'] != USER_TYPES['bank']['roles']['clerk']['num']:
        raise HTTPException(status_code=403, detail={'status': False, 'message': 'You are not authorized to perform this action'})
    req = do_entry_level_application_rejection(db=db, user_id=user['id'], loan_application_id=fields.loan_application_id, decline_reason=fields.decline_reason)
    if req['status'] == False:
        raise HTTPException(status_code=400, detail=req)
    return req

@router.post("/authorizer/approve", response_model=LoanResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def authorizer_approve(request: Request, fields: LoanApplicationApprovalModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    if user['role'] != USER_TYPES['bank']['roles']['auth']['num']:
        raise HTTPException(status_code=403, detail={'status': False, 'message': 'You are not authorized to perform this action'})
    req = do_authorizer_loan_application_approval(db=db, user_id=user['id'], loan_application_id=fields.loan_application_id)
    if req['status'] == False:
        raise HTTPException(status_code=400, detail=req)
    return req

@router.post("/authorizer/reject", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def authorizer_reject(request: Request, fields: LoanApplicationDeclineModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    if user['role'] != USER_TYPES['bank']['roles']['auth']['num']:
        raise HTTPException(status_code=403, detail={'status': False, 'message': 'You are not authorized to perform this action'})
    req = do_authorizer_loan_application_rejection(db=db, user_id=user['id'], loan_application_id=fields.loan_application_id, decline_reason=fields.decline_reason)
    if req['status'] == False:
        raise HTTPException(status_code=400, detail=req)
    return req
