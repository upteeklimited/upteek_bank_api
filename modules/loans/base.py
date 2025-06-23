from typing import Dict, Any
from sqlalchemy.orm import Session
from database.model import get_loans, get_single_loan_by_id
from modules.utils.tools import process_schema_dictionary, generate_slug
from fastapi_pagination.ext.sqlalchemy import paginate
import json

def retrieve_loans(db: Session, filters: Dict = {}):
    data = get_loans(db=db, filters=filters)
    return paginate(data)

def retrieve_single_loan(db: Session, id: int = 0):
    loan = get_single_loan_by_id(db=db, id=id)
    if loan is None:
        return {
            'status': False,
            'message': 'Loan not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': loan
        }
