from typing import Dict, List
from sqlalchemy.orm import Session
from database.model import create_notification
from fastapi_pagination.ext.sqlalchemy import paginate
import json

def notify_loan_application_rejection(db: Session, user_id: int=0, meta_data: Dict=None):
    if meta_data is not None:
        meta_data = json.dumps(meta_data)
    title = "Loan Application Rejected"
    body = "Your loan application has been rejected"
    return create_notification(db=db, user_id=user_id, title=title, body=body, meta_data=meta_data)

def notify_loan_application_accepted(db: Session, user_id: int=0, meta_data: Dict=None):
    if meta_data is not None:
        meta_data = json.dumps(meta_data)
    title = "Loan Disbursed"
    body = "Your loan application has been approved and disbursed"
    return create_notification(db=db, user_id=user_id, title=title, body=body, meta_data=meta_data)
