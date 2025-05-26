from typing import Dict
import dateparser
from sqlalchemy.orm import Session
from database.model import debit_account, create_account, debit_general_ledger_account, credit_general_ledger_account, credit_account, create_transaction, get_single_account_by_account_number, get_single_general_ledger_account_by_account_number, get_single_transaction_type_by_id, get_single_currency_by_code, get_single_country_by_code, get_single_transaction_by_id, get_single_transaction_by_reference, get_transactions, search_accounts, search_general_ledger_accounts
from modules.utils.tools import generate_transaction_reference, process_schema_dictionary
from modules.utils.acct import get_gl_ids_by_filters, get_account_ids_by_filters
from settings.constants import TRANSACTION_ACTIONS
from fastapi_pagination.ext.sqlalchemy import paginate

def create_general_posting(db: Session, transaction_type_id: int=0, from_account_number: str=None, to_account_number: str=None, amount: float=0, narration: str=None):
    country_id = 0
    country = get_single_country_by_code(db=db, code="NG")
    if country is not None:
        country_id = country.id
    currency_id = 0
    currency = get_single_currency_by_code(db=db, code="NGN")
    if currency is not None:
        currency_id = currency.id
    transaction_type = get_single_transaction_type_by_id(db=db, id=transaction_type_id)
    if transaction_type is None:
        return {
            'status': False,
            'message': 'Transaction type not found',
            'data': None,
        }
    else:
        reference = generate_transaction_reference(tran_type=transaction_type.name)
        from_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=from_account_number)
        to_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=to_account_number)
        from_acct = get_single_account_by_account_number(db=db, account_number=from_account_number)
        to_acct = get_single_account_by_account_number(db=db, account_number=to_account_number)
        main_trans = None
        from_done = False
        to_done = False
        type_action= transaction_type.action
        if type_action == 1:
            if from_gl is not None:
                dg_prev_balance = from_gl.balance
                dgl = debit_general_ledger_account(db=db, general_ledger_account_id=from_gl.id, amount=amount)
                if dgl['status'] == False:
                    return {
                        'status': False,
                        'message': dgl['message'],
                        'data': None
                    }
                else:
                    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=from_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=dg_prev_balance, new_balance=dgl['data']['balance'], status=1)
                    from_done = True
            if from_acct is not None:
                da_prev_balance = from_acct.available_balance
                da = debit_account(db=db, account_id=from_acct.id, amount=amount, override=True)
                if da['status'] == False:
                    return {
                        'status': False,
                        'message': da['message'],
                        'data': None
                    }
                main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=from_acct.user_id, merchant_id=from_acct.merchant_id, account_id=from_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=da_prev_balance, new_balance=da['data']['available_balance'], status=1)
                from_done = True
            if to_gl is not None:
                cgl_prvebalance = to_gl.balance
                cgl = credit_general_ledger_account(db=db, general_ledger_account_id=to_gl.id, amount=amount)
                if cgl['status'] == False:
                    return {
                        'status': False,
                        'message': cgl['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=to_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=cgl_prvebalance, new_balance=cgl['data']['balance'], status=1)
                to_done = True
            if to_acct is not None:
                ca_prev_balance = to_acct.available_balance
                ca = credit_account(db=db, account_id=to_acct.id, amount=amount)
                if ca['status'] == False:
                    return {
                        'status': False,
                        'message': ca['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=to_acct.user_id, merchant_id=to_acct.merchant_id, account_id=to_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=ca_prev_balance, new_balance=ca['data']['available_balance'], status=1)
                to_done = True
        elif type_action == 2:
            if from_gl is not None:
                dg_prev_balance = from_gl.balance
                dgl = credit_general_ledger_account(db=db, general_ledger_account_id=from_gl.id, amount=amount)
                if dgl['status'] == False:
                    return {
                        'status': False,
                        'message': dgl['message'],
                        'data': None
                    }
                else:
                    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=from_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=dg_prev_balance, new_balance=dgl['data']['balance'], status=1)
                    from_done = True
            if from_acct is not None:
                da_prev_balance = from_acct.available_balance
                da = credit_account(db=db, account_id=from_acct.id, amount=amount)
                if da['status'] == False:
                    return {
                        'status': False,
                        'message': da['message'],
                        'data': None
                    }
                main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=from_acct.user_id, merchant_id=from_acct.merchant_id, account_id=from_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=da_prev_balance, new_balance=da['data']['available_balance'], status=1)
                from_done = True
            if to_gl is not None:
                cgl_prvebalance = to_gl.balance
                cgl = debit_general_ledger_account(db=db, general_ledger_account_id=to_gl.id, amount=amount)
                if cgl['status'] == False:
                    return {
                        'status': False,
                        'message': cgl['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=to_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=cgl_prvebalance, new_balance=cgl['data']['balance'], status=1)
                to_done = True
            if to_acct is not None:
                ca_prev_balance = to_acct.available_balance
                ca = debit_account(db=db, account_id=to_acct.id, amount=amount, override=True)
                if ca['status'] == False:
                    return {
                        'status': False,
                        'message': ca['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=to_acct.user_id, merchant_id=to_acct.merchant_id, account_id=to_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=ca_prev_balance, new_balance=ca['data']['available_balance'], status=1)
                to_done = True
    if from_done == False:
        return {
            'status': False,
            'message': str(from_account_number) + " not found",
            'data': None
        }
    if to_done == False:
        return {
            'status': False,
            'message': str(to_account_number) + " not found",
            'data': None
        }
    if main_trans is None:
        return {
            'status': False,
            'message': 'Unexpected transaction failure',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': get_single_transaction_type_by_id(db=db, id=main_trans.id),
        }

def create_gl_to_gl_posting(db: Session, transaction_type_id: int=0, from_account_number: str=None, to_account_number: str=None, amount: float=0, narration: str=None):
    country_id = 0
    country = get_single_country_by_code(db=db, code="NG")
    if country is not None:
        country_id = country.id
    currency_id = 0
    currency = get_single_currency_by_code(db=db, code="NGN")
    if currency is not None:
        currency_id = currency.id
    transaction_type = get_single_transaction_type_by_id(db=db, id=transaction_type_id)
    if transaction_type is None:
        return {
            'status': False,
            'message': 'Transaction type not found',
            'data': None,
        }
    else:
        reference = generate_transaction_reference(tran_type=transaction_type.name)
        from_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=from_account_number)
        to_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=to_account_number)
        type_action = transaction_type.action

def retrieve_accounts(db: Session, search: str=None):
    resp = []
    if search is not None:
        accounts = search_accounts(db=db, search=search)
        if len(accounts) > 0:
            for account in accounts:
                resp.append({
                    'id': account.id,
                    'account_name': account.account_name,
                    'account_number': account.account_number,
                    'nuban': account.nuban,
                    'balance': account.available_balance,
                    'is_gl': False
                })
        gls = search_general_ledger_accounts(db=db, search=search)
        if len(gls) > 0:
            for gl in gls:
                resp.append({
                    'id': gl.id,
                    'account_name': gl.name,
                    'account_number': gl.account_number,
                    'nuban': None,
                    'balance': gl.balance,
                    'is_gl': True
                })
    return resp

def retrieve_transactions(db: Session, filters: Dict={}):
    if 'account_number' in filters:
        gl = get_single_general_ledger_account_by_account_number(db=db, account_number=filters['account_number'])
        if gl is not None:
            filters['gl_id'] = gl.id
        account = get_single_account_by_account_number(db=db, account_number=filters['account_number'])
        if account is not None:
            filters['account_id'] = account.id
    if 'account_name' in filters:
        gls = get_gl_ids_by_filters(db=db, filters={'name': filters['account_name']})
        if len(gls) > 0:
            filters['gl_ids'] = gls
        accounts = get_account_ids_by_filters(db=db, filters={'account_name': filters['account_name']})
        if len(accounts) > 0:
            filters['account_ids'] = accounts
    if 'from_date' in filters:
        if filters['from_date'] is not None:
            filters['from_date'] = dateparser.parse(filters['from_date'])
    if 'to_date' in filters:
        if filters['to_date'] is not None:
            filters['to_date'] = dateparser.parse(filters['to_date'])
    data = get_transactions(db=db, filters=filters)
    return paginate(data)

def retrieve_transaction_by_id(db: Session, transaction_id: int=0):
    trans = get_single_transaction_by_id(db=db, id=transaction_id)
    if trans is None:
        return {
            'status': False,
            'message': 'Transaction not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': trans,
        }
    