from typing import Optional, Any, List
from pydantic import BaseModel
from datetime import datetime
from schemas.acct import FinancialProductMiniModel, AccountInfoModel
from schemas.user import UserInfoModel, MerchantModel

class CreateLoanApplicationModel(BaseModel):
    product_id: int
    amount: float
    purpose: Optional[str] = None
    tenure: int
    interest_rate: float
    payment_data: Any

    class Config:
        orm_mode = True

class LoanApplicationMiniModel(BaseModel):
    id: int
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    account_id: Optional[int] = None
    card_id: Optional[int] = None
    amount: Optional[float] = None
    interest_amount: Optional[float] = None
    total_amount: Optional[float] = None
    purpose: Optional[str] = None
    tenure: Optional[int] = None
    interest_rate: Optional[float] = None
    moratorium: Optional[int] = None
    amount_after_moratorium: Optional[float] = None
    insurance: Optional[float] = None
    management_fee: Optional[float] = None
    loan_form_fee: Optional[float] = None
    loan_repayment_frequency: Optional[int] = None
    loan_savings_amount: Optional[float] = None
    loan_frequency_of_collection: Optional[int] = None
    installment_type: Optional[int] = None
    schedule_type: Optional[int] = None
    loan_data: Optional[str] = None
    character_data: Optional[str] = None
    capacity_data: Optional[str] = None
    capital_data: Optional[str] = None
    collateral_data: Optional[str] = None
    condition_data: Optional[str] = None
    payment_data: Optional[str] = None
    approval_level: Optional[int] = None
    decline_reason: Optional[str] = None
    status: Optional[int] = None  # 0 -> pending, 1 -> approved, 2 -> rejected, 3 -> cancelled.
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CollectionModel(BaseModel):
    id: int
    loan_id: int
    amount: Optional[float] = None
    total_principal: Optional[float] = None
    total_interest: Optional[float] = None
    bal_principal: Optional[float] = None
    bal_interest: Optional[float] = None
    retrial_num: Optional[int] = None
    retrial_status: Optional[int] = None
    status: Optional[int] = None
    collected_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class LoanModel(BaseModel):
    id: int
    application_id: Optional[int] = None
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    account_id: Optional[int] = None
    card_id: Optional[int] = None
    amount: Optional[float] = None
    unpaid_principal: Optional[float] = None
    unearned_interest: Optional[float] = None
    is_paid: Optional[int] = None
    is_provisioned: Optional[int] = None
    is_restructured: Optional[int] = None
    is_write_off: Optional[int] = None
    meta_data: Optional[str] = None
    status: Optional[int] = None
    past_due_at: Optional[datetime] = None
    doubtful_at: Optional[datetime] = None
    substandard_at: Optional[datetime] = None
    deliquent_at: Optional[datetime] = None
    provisioned_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    application: Optional[LoanApplicationMiniModel] = None
    collections: Optional[List[CollectionModel]] = None
    account: Optional[AccountInfoModel] = None
    loan_account: Optional[AccountInfoModel] = None
    user: Optional[UserInfoModel] = None
    merchant: Optional[MerchantModel] = None

    class Config:
        orm_mode = True

class LoanMiniModel(BaseModel):
    id: int
    application_id: Optional[int] = None
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    account_id: Optional[int] = None
    card_id: Optional[int] = None
    amount: Optional[float] = None
    unpaid_principal: Optional[float] = None
    unearned_interest: Optional[float] = None
    is_paid: Optional[int] = None
    is_provisioned: Optional[int] = None
    is_restructured: Optional[int] = None
    is_write_off: Optional[int] = None
    meta_data: Optional[str] = None
    status: Optional[int] = None
    past_due_at: Optional[datetime] = None
    doubtful_at: Optional[datetime] = None
    substandard_at: Optional[datetime] = None
    deliquent_at: Optional[datetime] = None
    provisioned_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class LoanApplicationModel(BaseModel):
    id: int
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    account_id: Optional[int] = None
    card_id: Optional[int] = None
    amount: Optional[float] = None
    interest_amount: Optional[float] = None
    total_amount: Optional[float] = None
    purpose: Optional[str] = None
    tenure: Optional[int] = None
    interest_rate: Optional[float] = None
    moratorium: Optional[int] = None
    amount_after_moratorium: Optional[float] = None
    insurance: Optional[float] = None
    management_fee: Optional[float] = None
    loan_form_fee: Optional[float] = None
    loan_repayment_frequency: Optional[int] = None
    loan_savings_amount: Optional[float] = None
    loan_frequency_of_collection: Optional[int] = None
    installment_type: Optional[int] = None
    schedule_type: Optional[int] = None
    loan_data: Optional[str] = None
    character_data: Optional[str] = None
    capacity_data: Optional[str] = None
    capital_data: Optional[str] = None
    collateral_data: Optional[str] = None
    condition_data: Optional[str] = None
    payment_data: Optional[str] = None
    approval_level: Optional[int] = None
    decline_reason: Optional[str] = None
    status: Optional[int] = None  # 0 -> pending, 1 -> approved, 2 -> rejected, 3 -> cancelled.
    created_at: Optional[datetime] = None
    financial_product: Optional[FinancialProductMiniModel] = None
    loan: Optional[LoanMiniModel] = None
    user: Optional[UserInfoModel] = None
    merchant: Optional[MerchantModel] = None

    class Config:
        orm_mode = True

class LoanApplicationResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[LoanApplicationModel] = None

    class Config:
        orm_mode = True

class CancelLoanApplicationModel(BaseModel):
    loan_application_id: int

    class Config:
        orm_mode = True

class LoanResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[LoanModel] = None

    class Config:
        orm_mode = True

class PayLoanModel(BaseModel):
    loan_id: int
    amount: float
    is_account: Optional[bool] = False
    is_card: Optional[bool] = False
    card_transaction_reference: Optional[str] = None
    provider_code: Optional[str] = None

    class Config:
        orm_mode = True

class LoanApplicationApprovalModel(BaseModel):
    loan_application_id: int

    class Config:
        orm_mode = True

class LoanApplicationDeclineModel(BaseModel):
    loan_application_id: int
    decline_reason: Optional[str] = None

    class Config:
        orm_mode = True

class LoanDataModel(BaseModel):
    total_loan_balance: Optional[float] = 0
    total_disbursed_loans: Optional[int] = 0
    total_overdue_loans: Optional[int] = 0
    total_overdue_loans_amount: Optional[float] = 0
    total_pending_loans_requests: Optional[int] = 0

    class Config:
        orm_mode = True

class LoanDataResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[LoanDataModel] = None

    class Config:
        orm_mode = True