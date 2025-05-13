from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_general_ledger_account_type, update_general_ledger_account_type, delete_general_ledger_account_type, get_last_general_ledger_account_type, get_single_general_ledger_account_type_by_id, get_single_general_ledger_account_type_by_account_code, get_general_ledger_account_types, get_single_country_by_code, get_single_currency_by_code
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.acct import generate_gl_type_code
from modules.utils.tools import process_schema_dictionary

def create_new_gl_type(db: Session, user_id: int = 0, name: str = None, description: str = None, type_number: int = 0):
    country_id = 0
    currency_id = 0
    country = get_single_country_by_code(db=db, code="NG")
    if country is not None:
        country_id = country.id
    currency = get_single_currency_by_code(db=db, code="NGN")
    if currency is not None:
        currency_id = currency.id
    last_id = 0
    last_type = get_last_general_ledger_account_type(db=db)
    if last_type is not None:
        last_id = last_type.id
    code = generate_gl_type_code(type_number=type_number, last_id=last_id)
    gl_type = create_general_ledger_account_type(db=db, country_id=country_id, currency_id=currency_id, name=name, description=description, account_code=code, type_number=type_number, status=1, created_by=user_id)
    return {
        'status': True,
        'message': 'Success',
        'data': gl_type,
    }

def update_existing_gl_type(db: Session, gl_type_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_general_ledger_account_type(db=db, id=gl_type_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_exisiting_gl_type(db: Session, gl_type_id: int=0):
    delete_general_ledger_account_type(db=db, id=gl_type_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_gl_types(db: Session, filters: Dict={}):
    data = get_general_ledger_account_types(db=db, filters=filters)
    return paginate(data)

def retrieve_single_gl_type(db: Session, gl_type_id: int=0):
    gl_type = get_single_general_ledger_account_type_by_id(db=db, id=gl_type_id)
    if gl_type is None:
        return {
            'status': False,
            'message': 'General Ledger Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl_type,
        }
    
def retrieve_single_gl_type_by_code(db: Session, code: str=None):
    gl_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=code)
    if gl_type is None:
        return {
            'status': False,
            'message': 'General Ledger Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl_type,
        }