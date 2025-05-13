from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_general_ledger_account, update_general_ledger_account, delete_general_ledger_account, get_single_general_ledger_account_type_by_id, get_last_general_ledger_account, get_general_ledger_accounts, get_single_general_ledger_account_by_id, get_single_general_ledger_account_by_account_number
from modules.utils.acct import generate_internal_gl_number
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.tools import process_schema_dictionary

def create_gl(db: Session, type_id: int=0, parent_id: int=0, name: str=None, description: str=None, created_by: int=0, authorized_by: int=0):
    last_gl = get_last_general_ledger_account(db=db)
    account_type = get_single_general_ledger_account_type_by_id(db=db, id=type_id)
    if account_type is None:
        return {
            'status': False,
            'message': 'Account type not found',
            'data': None
        }
    else:
        account_type_id = account_type.id
        account_type_code = account_type.account_code
        account_number = generate_internal_gl_number(type_code=account_type_code, last_id=last_gl.id)
        gl = create_general_ledger_account(db=db, type_id=account_type_id, parent_id=parent_id, name=name, description=description, account_number=account_number, status=1, created_by=created_by, authorized_by=authorized_by)
        return {
            'status': True,
            'message': 'Success',
            'data': gl
        }
    
def update_gl(db: Session, gl_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_general_ledger_account(db=db, id=gl_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_gl(db: Session, gl_id: int=0):
    delete_general_ledger_account(db=db, id=gl_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_gls(db: Session, filters: Dict={}):
    data = get_general_ledger_accounts(db=db, filters=filters)
    return paginate(data)

def retrieve_single_gl(db: Session, gl_id: int=0):
    gl = get_single_general_ledger_account_by_id(db=db, id=gl_id)
    if gl is None:
        return {
            'status': False,
            'message': 'General Ledger not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl,
        }
    
def retrieve_single_gl_by_account_number(db: Session, account_number: str=None):
    gl = get_single_general_ledger_account_by_account_number(db=db, account_number=account_number)
    if gl is None:
        return {
            'status': False,
            'message': 'General Ledger not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl,
        }