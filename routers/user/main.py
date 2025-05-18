from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from modules.authentication.auth import auth
from modules.users.manage import create_a_new_user, update_user_details, retrieve_users, retrieve_customers, retrieve_users_by_search, retrieve_customers_by_search, retrieve_single_user
from database.schema import CreateUserModel, UpdateUserModel, UserMainModel, UpdateUserPasswordModel, UserMainResponseModel, ErrorResponse, PlainResponse
from fastapi_pagination import LimitOffsetPage, Page
from settings.constants import USER_TYPES

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create", response_model=UserMainResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateUserModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    req = create_a_new_user(db=db, username=fields.username, email=fields.email, phone_number=fields.phone_number, password=fields.password, role=fields.role, first_name=fields.first_name, other_name=fields.other_name, last_name=fields.last_name)
    return req

@router.post("/update/{user_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateUserModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), user_id: int = 0):
    values = fields.model_dump()
    req = update_user_details(db=db, user_id=user_id, values=values)
    return req

@router.get("/get_all", response_model=Page[UserMainModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return retrieve_users(db=db)

@router.get("/customers", response_model=Page[UserMainModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def customers(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return retrieve_customers(db=db)

@router.get("/search", response_model=Page[UserMainModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), username: str = None, email: str = None, phone_number: str = None, status: int = None):
    filters = {
        'user_type': USER_TYPES['bank']['num']
    }
    if username is not None:
        filters['username'] = username
    if email is not None:
        filters['email'] = email
    if phone_number is not None:
        filters['phone_number'] = phone_number
    if status is not None:
        if status > 0:
            filters['status'] = status
    return retrieve_users_by_search(db=db, filters=filters)

@router.get("/customers/search", response_model=Page[UserMainModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def customers_search(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), username: str = None, email: str = None, phone_number: str = None, status: int = None):
    filters = {}
    if username is not None:
        filters['username'] = username
    if email is not None:
        filters['email'] = email
    if phone_number is not None:
        filters['phone_number'] = phone_number
    if status is not None:
        if status > 0:
            filters['status'] = status
    return retrieve_customers_by_search(db=db, filters=filters)

@router.get("/get_single/{user_id}", response_model=UserMainResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db), user_id: int = 0):
    return retrieve_single_user(db=db, user_id=user_id)
