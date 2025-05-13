from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_transaction_type, update_transaction_type, delete_transaction_type, get_transaction_types, get_single_transaction_type_by_id, get_single_transaction_type_by_code
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.tools import generate_transaction_type_code, process_schema_dictionary

def create_new_transaction_type(db: Session, user_id: int = 0, corresponding_gl_id: int = 0, charge_gl_id: int = 0, name: str = None, description: str = None, action: int = 0, chargeable: int = 0, charge_type: int = 0, charge_percentage: float = 0, charge_flat: float = 0, require_approval: int = 0, require_approval_amount: float = 0):
    code = generate_transaction_type_code(db=db)
    trans_type = create_transaction_type(db=db, corresponding_gl_id=corresponding_gl_id, charge_gl_id=charge_gl_id, name=name, description=description, code=code, action=action, chargeable=chargeable, charge_type=charge_type, charge_percentage=charge_percentage, charge_flat=charge_flat, require_approval=require_approval, require_approval_amount=require_approval_amount, status=1, created_by=user_id)
    return {
        'status': True,
        'message': 'Success',
        'data': trans_type,
    }

def update_existing_transaction_type(db: Session, type_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_transaction_type(db=db, id=type_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_existing_transaction_type(db: Session, type_id: int=0):
    delete_transaction_type(db=db, id=type_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrive_transaction_type(db: Session, filters: Dict={}):
    data = get_transaction_types(db=db, filters=filters)
    return paginate(data)

def retrieve_single_transaction_type(db: Session, type_id: int=0):
    trans_type = get_single_transaction_type_by_id(db=db, id=type_id)
    if trans_type is None:
        return {
            'status': False,
            'message': 'Transaction Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': trans_type,
        }
    
def retrieve_single_transaction_type_by_code(db: Session, code: str=None):
    trans_type = get_single_transaction_type_by_code(db=db, code=code)
    if trans_type is None:
        return {
            'status': False,
            'message': 'Transaction Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': trans_type,
        }