from typing import Dict, Any
from sqlalchemy.orm import Session
from database.model import get_loans, get_single_loan_by_id, sum_of_account_balances, count_loan_applications, count_loans, sum_of_overdue_collections, count_loans_with_pending_collections
from modules.utils.tools import process_schema_dictionary, generate_slug
from fastapi_pagination.ext.sqlalchemy import paginate

def get_loan_data(db: Session):
    total_loan_balance = sum_of_account_balances(db=db, filters={'product_type': 4})
    total_disbursed_loans = count_loans(db=db)
    total_overdue_loans = count_loans_with_pending_collections(db=db)
    total_overdue_loans_amount = sum_of_overdue_collections(db=db)
    total_pending_loans_requests = count_loan_applications(db=db, filters={'status': 0})
    data = {
        'total_loan_balance': total_loan_balance,
        'total_disbursed_loans': total_disbursed_loans,
        'total_overdue_loans': total_overdue_loans,
        'total_overdue_loans_amount': total_overdue_loans_amount,
        'total_pending_loans_requests': total_pending_loans_requests,
    }
    return {
        'status': True,
        'message': 'Success',
        'data': data,
    }

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
