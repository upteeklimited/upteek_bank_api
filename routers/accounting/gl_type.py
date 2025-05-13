from fastapi import APIRouter, Request, Depends
from modules.authentication.auth import auth
from modules.accounting.gl_types import create_new_gl_type, update_existing_gl_type, delete_exisiting_gl_type, retrieve_gl_types, retrieve_single_gl_type, retrieve_single_gl_type_by_code
from database.schema import ErrorResponse, PlainResponse, GLTypeModel, CreateGLTypeModel, UpdateGLTypeModel, GLTypeResponseModel
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/general_ledger_types",
    tags=["general_ledger_types"]
)


@router.post("/create", response_model=GLTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateGLTypeModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper)):
    req = create_new_gl_type(db=db, user_id=user['id'], name=fields.name, description=fields.description, type_number=fields.type_number)
    return req

@router.post("/update/{type_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateGLTypeModel, db: Session = Depends(get_db), user=Depends(auth.auth_wrapper), type_id: int=0):
    values = fields.model_dump()
    req = update_existing_gl_type(db=db, gl_type_id=type_id, values=values)
    return req

@router.get("/delete/{type_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return delete_exisiting_gl_type(db=db, gl_type_id=type_id)

@router.get("/", response_model=Page[GLTypeModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, db: Session = Depends(get_db), name: str = None, account_code: str = None, status: int = 0):
    filters = {}
    if name is not None:
        filters['name'] = name
    if account_code is not None:
        filters['account_code'] = account_code
    if status is not None:
        if  status > 0:
            filters['status'] = status
    return retrieve_gl_types(db=db, filters=filters)

@router.get("/get_single/{type_id}", response_model=GLTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), type_id: int = 0):
    return retrieve_single_gl_type(db=db, gl_type_id=type_id)

@router.get("/get_single_by_code/{code}", response_model=GLTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single_by_code(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), code: str = None):
    return retrieve_single_gl_type_by_code(db=db, code=code)

