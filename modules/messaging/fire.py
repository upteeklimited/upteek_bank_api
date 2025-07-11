from typing import Dict, List
from modules.external.firebase import send_push, send_push_multi

def fb_loan_application_rejection(token: str=None, data: Dict={}):
    data['name'] = "loan_app_rejection"
    title = "Loan Application Rejected"
    body = "Your loan application has been rejected"
    return send_push(token=token, title=title, body=body, data=data)

def fb_loan_application_accepted(token: str=None, data: Dict={}):
    data['name'] = "loan_disbursed"
    title = "Loan Disbursed"
    body = "Your loan application has been approved and disbursed"
    return send_push(token=token, title=title, body=body, data=data)
