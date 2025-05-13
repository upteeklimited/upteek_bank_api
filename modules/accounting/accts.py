from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_accounts, get_single_account_by_id, get_single_account_by_account_number
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_accounts(db: Session, filters: Dict={}):
    data = get_accounts(db=db, filters=filters)
    return paginate(data)

def retrieve_single_account(db: Session, account_id: int=0):
    account = get_single_account_by_id(db=db, id=account_id)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account,
        }

def retrieve_single_account_by_number(db: Session, account_number: str=None):
    account = get_single_account_by_account_number(db=db, account_number=account_number)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account,
        }