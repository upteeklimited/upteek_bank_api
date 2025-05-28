from typing import Dict
from sqlalchemy.orm import Session
from database.model import count_customers, count_merchants, count_customers_and_merchants, sum_of_deposits, count_of_deposits, sum_of_loans, count_accounts


def get_dashboard_data(db: Session):
    customers_count = count_customers(db=db)
    merchants_count = count_merchants(db=db)
    customers_and_merchants_count = count_customers_and_merchants(db=db)
    total_deposits = sum_of_deposits(db=db)
    total_deposits_count = count_of_deposits(db=db)
    total_loans = sum_of_loans(db=db, filters={'status': 1})
    total_accounts = count_accounts(db=db)
    data =  {
        "customers_count": customers_count,
        "merchants_count": merchants_count,
        "customers_and_merchants_count": customers_and_merchants_count,
        "total_deposits": total_deposits,
        "total_deposits_count": total_deposits_count,
        "total_loans": total_loans,
        "total_accounts": total_accounts
    }
    return {
        'status': True,
        'message': 'Success',
        'data': data
    }