from typing import Dict, Any
from sqlalchemy.orm import Session
from database.model import create_loan_application, update_loan_application, get_single_loan_application_by_id, get_loan_applications, get_single_user_primary_account, get_just_single_loan_application_by_id, get_just_single_loan_by_id, get_just_single_financial_product_by_id, get_single_currency_by_id
from modules.utils.tools import process_schema_dictionary, generate_slug
from fastapi_pagination.ext.sqlalchemy import paginate
import json

def retrieve_loan_applications(db: Session, filters: Dict={}):
    data = get_loan_applications(db=db, filters=filters)
    return paginate(data)

def retrieve_single_loan_application(db: Session, id: int=0):
    loan_application = get_single_loan_application_by_id(db=db, id=id)
    if loan_application is None:
        return {
            'status': False,
            'message': 'Loan application not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': loan_application
        }