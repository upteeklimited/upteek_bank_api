from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from modules.authentication.auth import auth
from modules.dash.board import get_dashboard_data
from database.schema import DashboardDataResponseModel, ErrorResponse, PlainResponse
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get("/data", response_model=DashboardDataResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return get_dashboard_data(db=db)
