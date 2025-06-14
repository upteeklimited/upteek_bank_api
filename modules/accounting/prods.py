from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_financial_product, FinancialProduct, create_general_ledger_account, get_single_general_ledger_account_type_by_account_code, get_last_general_ledger_account, update_financial_product, get_single_product_by_id, create_account_type, get_last_account_type, get_single_financial_product_by_id, get_financial_products, update_account_type, get_single_country_by_code, get_single_currency_by_code, get_single_account_type_by_product_id, delete_financial_product, delete_account_type
from modules.utils.acct import generate_internal_gl_number, generate_account_type_code
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.tools import process_schema_dictionary
import json


def create_product_gls(db: Session, product: FinancialProduct, created_by: int=0, authorized_by: int=0):
    product_type = product.product_type
    product_name = product.name
    reporting_gl_id = 0
    overdraft_gl_id = 0
    expense_gl_id = 0
    overdrawn_interest_gl_id = 0
    interest_receivable_gl_id = 0
    interest_payable_gl_id = 0
    income_gl_id = 0
    unearned_gl_id = 0
    fixed_gl_id = 0
    insurance_gl_id = 0
    last_gl_id = 0
    last_gl = get_last_general_ledger_account(db=db)
    if last_gl is not None:
        last_gl_id = last_gl.id
    asset_type_id = 0
    asset_account_code = "10000000"
    asset_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=asset_account_code)
    if asset_type is not None:
        asset_type_id = asset_type.id
    liability_account_code = "20000000"
    liability_type_id = 0
    liability_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=liability_account_code)
    if liability_type is not None:
        liability_type_id = liability_type.id
    income_account_code = "40000000"
    income_type_id = 0
    income_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=income_account_code)
    if income_type is not None:
        income_type_id = income_type.id
    expense_account_code = "50000000"
    expense_type_id = 0
    expense_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=expense_account_code)
    if expense_type is not None:
        expense_type_id = expense_type.id
    reporting_gl_name = product_name + " Reporting General Ledger "
    overdraft_gl_name = product_name + " Overdraft General Ledger "
    interest_expense_gl_name = product_name + "Interest Expense General Ledger "
    interest_income_gl_name = product_name + " Interest Income General Ledger "
    overdrawn_interest_income_gl_name = product_name + " Overdrawn Interest Income General Ledger "
    interest_receivable_gl_name = product_name + " Interest Receivable General Ledger "
    interest_payable_gl_name = product_name + " Interest Payable General Ledger "
    interest_unearned_gl_name = product_name + " Unearned Interest General Ledger "
    fixed_charge_gl_name = product_name + " Fixed Charge General Ledger "
    insurance_holding = product_name + " Insurance Holding "
    if product_type == 1:
        #savings        
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        overdraft_gl = create_general_ledger_account(db=db, type_id=asset_type_id, name=overdraft_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        overdraft_gl_id = overdraft_gl.id
        last_gl_id = overdraft_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        overdrawn_interest = create_general_ledger_account(db=db, type_id=income_type_id, name=overdrawn_interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        overdrawn_interest_gl_id = overdrawn_interest.id
        last_gl_id = overdrawn_interest_gl_id

        interest_receivable = create_general_ledger_account(db=db, type_id=asset_type_id, name=interest_receivable_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        interest_receivable_gl_id = interest_receivable.id
        last_gl_id = interest_receivable_gl_id

        interest_payable = create_general_ledger_account(db=db, type_id=liability_type_id, name=interest_payable_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        interest_payable_gl_id = interest_payable.id
        last_gl_id = interest_payable_gl_id
    elif product_type == 2:
        #current
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        overdraft_gl = create_general_ledger_account(db=db, type_id=asset_type_id, name=overdraft_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        overdraft_gl_id = overdraft_gl.id
        last_gl_id = overdraft_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        interest_income = create_general_ledger_account(db=db, type_id=income_type_id, name=interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        income_gl_id = interest_income.id
        last_gl_id = income_gl_id

        overdrawn_interest = create_general_ledger_account(db=db, type_id=income_type_id, name=overdrawn_interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        overdrawn_interest_gl_id = overdrawn_interest.id
        last_gl_id = overdrawn_interest_gl_id

        interest_receivable = create_general_ledger_account(db=db, type_id=asset_type_id, name=interest_receivable_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        interest_receivable_gl_id = interest_receivable.id
        last_gl_id = interest_receivable_gl_id

        interest_payable = create_general_ledger_account(db=db, type_id=liability_type_id, name=interest_payable_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        interest_payable_gl_id = interest_payable.id
        last_gl_id = interest_payable_gl_id
    elif product_type == 3:
        #deposit
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id
    elif product_type == 4:
        #loan
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        interest_income = create_general_ledger_account(db=db, type_id=income_type_id, name=interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        income_gl_id = interest_income.id
        last_gl_id = income_gl_id

        unearned_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_unearned_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        unearned_gl_id = unearned_gl.id
        last_gl_id = unearned_gl_id

        fixed_gl = create_general_ledger_account(db=db, type_id=income_type_id, name=fixed_charge_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        fixed_gl_id = fixed_gl.id
        last_gl_id = fixed_gl_id

        insurance_gl = create_general_ledger_account(db=db, type_id=income_type_id, name=insurance_holding, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        insurance_gl_id = insurance_gl.id
        last_gl_id = insurance_gl_id
    
    data = {
        'reporting_gl_id': reporting_gl_id,
        'overdraft_gl_id': overdraft_gl_id,
        'expense_gl_id': expense_gl_id,
        'overdrawn_interest_gl_id': overdrawn_interest_gl_id,
        'interest_receivable_gl_id': interest_receivable_gl_id,
        'interest_payable_gl_id': interest_payable_gl_id,
        'income_gl_id': income_gl_id,
        'unearned_gl_id': unearned_gl_id,
        'fixed_gl_id': fixed_gl_id,
        'insurance_gl_id': insurance_gl_id,
    }
    return {
        'status': True,
        'message': 'Success',
        'data': data
    }

def create_new_financial_product(db: Session, name: str=None, description: str=None, product_type: int=0, user_type: int=0, individual_compliance_type: int=0, merchant_compliance_type: int=0, interest_rate: float=0, overdrawn_interest_rate: float=0, charge_if_overdrawn: float=0, charges: float=0, cot_rate: float=0, minimum_amount: float=0, maximum_amount: float=0, liquidation_penalty: float=0, tenure: int=0, interest_tenure_type: int = 0, interest_tenure_data: str = None, guarantor_requirement: int=0, amount_to_require_guarantor: float=0, created_by: int=0, authorized_by: int=0):
    country_id = 0
    currency_id = 0
    country = get_single_country_by_code(db=db, code="NG")
    if country is not None:
        country_id = country.id
    currency = get_single_currency_by_code(db=db, code="NGN")
    if currency is not None:
        currency_id = currency.id
    product = create_financial_product(db=db, name=name, description=description, country_id=country_id, currency_id=currency_id, product_type=product_type, user_type=user_type, individual_compliance_type=individual_compliance_type, merchant_compliance_type=merchant_compliance_type, interest_rate=interest_rate, overdrawn_interest_rate=overdrawn_interest_rate, charge_if_overdrawn=charge_if_overdrawn, charges=charges, cot_rate=cot_rate, minimum_amount=minimum_amount, maximum_amount=maximum_amount, liquidation_penalty=liquidation_penalty, tenure=tenure, interest_tenure_type=interest_tenure_type, interest_tenure_data=json.dumps(interest_tenure_data), guarantor_requirement=guarantor_requirement, amount_to_require_guarantor=amount_to_require_guarantor, status=1, created_by=created_by, authorized_by=authorized_by)
    resp = create_product_gls(db=db, product=product, created_by=created_by, authorized_by=authorized_by)
    resp_data = resp['data']
    values = {
        'gl_id': resp_data['reporting_gl_id'],
        'interest_expense_gl_id': resp_data['interest_payable_gl_id'],
        'interest_income_gl_id': resp_data['income_gl_id'],
        'principal_unpaid_gl_id': resp_data['expense_gl_id'],
        'interest_unearned_gl_id': resp_data['unearned_gl_id'],
        'fixed_charge_gl_id': resp_data['fixed_gl_id'],
        'insurance_holding_gl_id': resp_data['insurance_gl_id'],
        'overdrawn_interest_gl_id': resp_data['overdrawn_interest_gl_id'],
        'liability_overdraft_gl_id': resp_data['overdraft_gl_id'],
        'interest_receivable_gl_id': resp_data['interest_receivable_gl_id'],
        'interest_payable_gl_id': resp_data['interest_payable_gl_id'],
    }
    update_financial_product(db=db, id=product.id, values=values)
    last_account_type_id = 0
    last_account_type = get_last_account_type(db=db)
    if last_account_type is not None:
        last_account_type_id = last_account_type.id
    account_type_code = generate_account_type_code(product_type=product_type, last_id=last_account_type_id)
    create_account_type(db=db, product_id=product.id, name=name, account_code=account_type_code, status=1, created_by=created_by, authorized_by=authorized_by)
    return {
        'status': True,
        'message': 'Success',
        'data': get_single_product_by_id(db=db, id=product.id)
    }

def update_existing_financial_product(db: Session, product_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    type_vals = {}
    if 'name' in values:
        type_vals['name'] = values['name']
    if 'description' in values:
        type_vals['description'] = values['description']
    if 'status' in values:
        type_vals['status'] = values['status']
    if 'interest_tenure_data' in values:
        if values['interest_tenure_data'] is not None:
            values['interest_tenure_data'] = json.dumps(values['interest_tenure_data'])
    update_financial_product(db=db, id=product_id, values=values)
    if type_vals != {}:
        account_type = get_single_account_type_by_product_id(db=db, product_id=product_id)
        if account_type is not None:
            update_account_type(db=db, id=account_type.id, values=type_vals)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_existing_financial_product(db: Session, product_id: int=0):
    delete_financial_product(db=db, id=product_id)
    account_type = get_single_account_type_by_product_id(db=db, product_id=product_id)
    if account_type is not None:
        delete_account_type(db=db, id=account_type.id)
    return {
        'status': True,
        'message': 'Success',
    }

def retrieve_financial_products(db: Session, filters: Dict={}):
    data = get_financial_products(db=db, filters=filters)
    return paginate(data)

def retrieve_single_financial_product(db: Session, product_id: int=0):
    product = get_single_financial_product_by_id(db=db, id=product_id)
    if product is None:
        return {
            'status': False,
            'message': 'Financial Product not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': product,
        }