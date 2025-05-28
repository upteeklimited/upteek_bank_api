from typing import Dict
from sqlalchemy.orm import Session
from database.model import count_customers, count_merchants, count_customers_and_merchants, sum_of_deposits, count_of_deposits, sum_of_loans, count_accounts, get_dashboard_transactions_data
from calendar import month_name


def get_dashboard_data(db: Session):
    customers_count = count_customers(db=db)
    merchants_count = count_merchants(db=db)
    customers_and_merchants_count = count_customers_and_merchants(db=db)
    total_deposits = sum_of_deposits(db=db)
    total_deposits_count = count_of_deposits(db=db)
    active_loans = sum_of_loans(db=db, filters={'status': 1})
    total_accounts = count_accounts(db=db)
    data =  {
        "customers_count": customers_count,
        "merchants_count": merchants_count,
        "customers_and_merchants_count": customers_and_merchants_count,
        "total_deposits": total_deposits,
        "total_deposits_count": total_deposits_count,
        "active_loans": active_loans,
        "total_accounts": total_accounts
    }
    return {
        'status': True,
        'message': 'Success',
        'data': data
    }

def generate_dashboard_graph_data(db: Session):
    month = 6
    results = get_dashboard_transactions_data(db=db, month=month)
    graph_data = []
    for result in results:
        month_name_str = month_name[int(result.month)]
        graph_data.append({
            "month": month_name_str,
            "credit": int(result.credit or 0),
            "debit": int(result.debit or 0)
        })
    return {
        'status': True,
        'message': 'Success',
        'data': graph_data
    }