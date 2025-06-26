from typing import Dict, Any
from sqlalchemy.orm import Session
from database.model import update_loan_application, get_single_loan_application_by_id, get_loan_applications, get_single_user_by_id, get_just_single_loan_application_by_id, get_just_single_loan_by_id, get_just_single_financial_product_by_id, get_single_currency_by_id, create_loan_application_log, get_single_account_type_by_product_id, get_single_transaction_type_by_code, create_loan, debit_account, create_transaction, credit_account, get_just_single_account_by_id, create_collection, get_single_loan_by_id
from modules.accounting.accts import create_new_customer_account
from modules.utils.tools import rand_upper_string_generator, generate_transaction_reference, is_valid_json, format_date_laravel_datetime
from fastapi_pagination.ext.sqlalchemy import paginate
from database.db import get_laravel_datetime
from settings.constants import TRANSACTION_ACTIONS
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

def do_entry_level_application_approval(db: Session, user_id: int=0, loan_application_id: int=0):
    loan_application = get_just_single_loan_application_by_id(db=db, id=loan_application_id)
    if loan_application is None:
        return {
            'status': False,
            'message': 'Loan application not found'
        }
    else:
        if loan_application.status > 0:
            return {
                'status': False,
                'message': 'Loan application already processed',
            }
        approval_level = loan_application.approval_level
        if approval_level > 1:
            return {
                'status': False,
                'message': 'Loan application already approved beyond entry level',
            }
        create_loan_application_log(db=db, application_id=loan_application_id, approved_user_id=user_id, approval_level=2, status=1, approved_at=get_laravel_datetime())
        update_loan_application(db=db, id=loan_application_id, values={
            'approval_level': 2,
        })
        return {
            'status': True,
            'message': 'Success',
        }
    
def do_entry_level_application_rejection(db: Session, user_id: int=0, loan_application_id: int=0, decline_reason: str=None):
    loan_application = get_just_single_loan_application_by_id(db=db, id=loan_application_id)
    if loan_application is None:
        return {
            'status': False,
            'message': 'Loan application not found'
        }
    else:
        if loan_application.status > 0:
            return {
                'status': False,
                'message': 'Loan application already processed',
            }
        approval_level = loan_application.approval_level
        if approval_level > 1:
            return {
                'status': False,
                'message': 'Loan application already approved beyond entry level',
            }
        create_loan_application_log(db=db, application_id=loan_application_id, rejected_user_id=user_id, approval_level=2, decline_reason=decline_reason, status=1, rejected_at=get_laravel_datetime())
        update_loan_application(db=db, id=loan_application_id, values={
            'approval_level': 1,
            'decline_reason': decline_reason,
            'status': 2
        })
        return {
            'status': True,
            'message': 'Success',
        }
    
def do_authorizer_loan_application_rejection(db: Session, user_id: int=0, loan_application_id: int=0, decline_reason: str=None):
    loan_application = get_just_single_loan_application_by_id(db=db, id=loan_application_id)
    if loan_application is None:
        return {
            'status': False,
            'message': 'Loan application not found'
        }
    else:
        if loan_application.status > 0:
            return {
                'status': False,
                'message': 'Loan application already processed',
            }
        approval_level = loan_application.approval_level
        if approval_level < 2:
            return {
                'status': False,
                'message': 'Loan application not yet approved at entry level',
            }
        create_loan_application_log(db=db, application_id=loan_application_id, rejected_user_id=user_id, approval_level=approval_level, decline_reason=decline_reason, status=1, rejected_at=get_laravel_datetime())
        update_loan_application(db=db, id=loan_application_id, values={
            'approval_level': 1,
            'decline_reason': decline_reason,
            'status': 0
        })
        return {
            'status': True,
            'message': 'Success',
        }
    
def do_authorizer_loan_application_approval(db: Session, user_id: int=0, loan_application_id: int=0):
    loan_application = get_just_single_loan_application_by_id(db=db, id=loan_application_id)
    if loan_application is None:
        return {
            'status': False,
            'message': 'Loan application not found',
                'data': None
        }
    else:
        if loan_application.status > 0:
            return {
                'status': False,
                'message': 'Loan application already processed',
                'data': None
            }
        approval_level = loan_application.approval_level
        if approval_level < 2:
            return {
                'status': False,
                'message': 'Loan application not yet approved at entry level',
                'data': None
            }
        financial_product = get_just_single_financial_product_by_id(db=db, id=loan_application.product_id)
        if financial_product is None:
            return {
                'status': False,
                'message': 'Financial product not found',
                'data': None
            }
        account_type = get_single_account_type_by_product_id(db=db, product_id=financial_product.id)
        if account_type is None:
            return {
                'status': False,
                'message': 'Account type not found',
                'data': None
            }
        customer_user = get_single_user_by_id(db=db, id=loan_application.user_id)
        if customer_user is None:
            return {
                'status': False,
                'message': 'Customer user not found',
                'data': None
            }
        account = get_just_single_account_by_id(db=db, id=loan_application.account_id)
        if account is None:
            return {
                'status': False,
                'message': 'Receiving account not found',
                'data': None
            }
        payment_data = loan_application.payment_data
        if is_valid_json(payment_data) == False:
            return {
                'status': False,
                'message': 'Could not process payment timetable data',
                'data': None
            }
        collection_data = json.loads(payment_data)
        loan_acct_name = "Loan Account #" + rand_upper_string_generator()
        loan_acc_req = create_new_customer_account(db=db, user_id=user_id, merchant_id=customer_user.merchant_id, account_type_id=account_type.id, account_name=loan_acct_name)
        if loan_acc_req['status'] == False:
            return {
                'status': False,
                'message': loan_acc_req['message'],
                'data': None
            }
        new_loan_acct = loan_acc_req['data']
        loan_account_id = new_loan_acct.id
        trans_debit = get_single_transaction_type_by_code(db=db, code="009")
        # trans_credit = get_single_transaction_type_by_code(db=db, code="010")
        reference = generate_transaction_reference(tran_type=trans_debit.name)
        interest = (loan_application.interest_rate/100)* loan_application.amount
        interest = round(interest, 2)
        currency_id = financial_product.currency_id
        loan = create_loan(db=db, user_id=customer_user.id, merchant_id=customer_user.merchant_id, application_id=loan_application_id, account_id=account.id, gl_account_id=financial_product.gl_id, amount=loan_application.amount, unpaid_principal=loan_application.amount, unearned_interest=interest, status=1)
        da = debit_account(db=db, account_id=loan_account_id, amount=loan_application.amount, override=True)
        if da['status'] == False:
            return {
                'status': False,
                'message': da['message'],
                'data': None
            }
        create_transaction(db=db, country_id=customer_user.country_id, currency_id=currency_id, user_id=customer_user.id, merchant_id=customer_user.merchant_id, account_id=loan_account_id, type_id=trans_debit.id, loan_id=loan.id, action=TRANSACTION_ACTIONS['debit'], reference=reference, narration="Loan Disbursement", amount=loan_application.amount, previous_balance=0, new_balance=da['data']['available_balance'], status=1, created_by=user_id)
        acct_prev_balance = account.available_balance
        ca = credit_account(db=db, account_id=account.id, amount=loan_application.amount)
        if ca['status'] == False:
            return {
                'status': False,
                'message': ca['message'],
                'data': None
            }
        create_transaction(db=db, country_id=customer_user.country_id, currency_id=currency_id, user_id=customer_user.id, merchant_id=customer_user.merchant_id, account_id=account.id, type_id=trans_debit.id, loan_id=loan.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, narration="Loan Disbursement", amount=loan_application.amount, previous_balance=acct_prev_balance, new_balance=ca['data']['available_balance'], status=1, created_by=user_id)
        if len(collection_data) > 0:
            for collection in collection_data:
                principal = 0
                if 'principal' in collection:
                    principal = collection['principal']
                interest = 0
                if 'interest' in collection:
                    interest = collection['interest']
                amount = 0
                if 'amount' in collection:
                    amount = collection['amount']
                due_date = None
                if 'date' in collection:
                    due_date = format_date_laravel_datetime(date_str=collection['date'])
                create_collection(db=db, loan_id=loan.id, amount=amount, total_principal=principal, total_interest=interest, bal_principal=principal, bal_interest=interest, status=0, collected_at=due_date)
        create_loan_application_log(db=db, application_id=loan_application_id, approved_user_id=user_id, approval_level=3, status=1, approved_at=get_laravel_datetime())
        update_loan_application(db=db, id=loan_application_id, values={
            'approval_level': 3,
        })
        return {
            'status': True,
            'message': 'Success',
            'data': get_single_loan_by_id(db=db, id=loan.id)
        }