from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_single_deposit_by_id, get_deposits
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_deposits(db: Session, filters: Dict={}):
    data = get_deposits(db=db, filters=filters)
    return paginate(data)

def retrieve_single_deposit(db: Session, deposit_id: int=0):
    deposit = get_single_deposit_by_id(db=db, id=deposit_id)
    if deposit is None:
        return {
            'status': False,
            'message': 'Deposit not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': deposit,
        }