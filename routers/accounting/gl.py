from fastapi import APIRouter, Request, Depends, Query
from modules.authentication.auth import auth
from modules.accounting.gls import create_gl, update_gl, delete_gl, retrieve_gls, retrieve_single_gl, retrieve_single_gl_by_account_number
from database.schema import ErrorResponse, PlainResponse, GLModel, CreateGLModel, UpdateGLModel, GLResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/general_ledger",
    tags=["general_ledger"]
)


@router.post("/create", response_model=GLResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateGLModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_gl(db=db, type_id=fields.type_id, parent_id=fields.parent_id, name=fields.name, description=fields.description, created_by=user['id'])
    return req

@router.post("/update/{gl_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateGLModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), gl_id: int=0):
    values = fields.model_dump()
    req = update_gl(db=db, gl_id=gl_id, values=values)
    return req

@router.get("/delete/{gl_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), gl_id: int = 0):
    return delete_gl(db=db, gl_id=gl_id)

@router.get("/", response_model=Page[GLModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), name: str = Query(None), account_number: str = Query(None), status: int = Query(None), type_id: int = Query(None), parent_id: int = Query(None), manager_id: int = Query(None)):
    filters = {}
    if name:
        filters['name'] = name
    if account_number:
        filters['account_number'] = account_number
    if status:
        filters['status'] = status
    if type_id:
        filters['type_id'] = type_id
    if parent_id:
        filters['parent_id'] = parent_id
    if manager_id:
        filters['manager_id'] = manager_id
    return retrieve_gls(db=db, filters=filters)

@router.get("/get_single/{gl_id}", response_model=GLResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), gl_id: int = 0):
    return retrieve_single_gl(db=db, gl_id=gl_id)

@router.get("/get_single_by_code/{account_number}", response_model=GLResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_by_code(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), account_number: str = None):
    return retrieve_single_gl_by_account_number(db=db, account_number=account_number)

