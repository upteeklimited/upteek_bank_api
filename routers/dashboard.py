from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from modules.authentication.auth import auth
from modules.dash.board import get_dashboard_data, generate_dashboard_graph_data
from database.schema import DashboardDataResponseModel, DashboardGraphDataResponseModel, ErrorResponse, PlainResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get("/data", response_model=DashboardDataResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def dashboard_data(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return get_dashboard_data(db=db)

@router.get("/graph", response_model=DashboardGraphDataResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def dashboard_data(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return generate_dashboard_graph_data(db=db)
