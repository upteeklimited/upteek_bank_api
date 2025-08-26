from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Collection(Base):

    __tablename__ = "collections"
     
    id = Column(BigInteger, primary_key=True, index=True)
    loan_id = Column(BigInteger, ForeignKey("loans.id"))
    amount = Column(Float, default=0)
    total_principal = Column(Float, default=0)
    total_interest = Column(Float, default=0)
    bal_principal = Column(Float, default=0)
    bal_interest = Column(Float, default=0)
    retrial_num = Column(Integer, default=0)
    retrial_status = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    collected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    loan = relationship('Loan', back_populates='collections', uselist=False)

def create_collection(db: Session, loan_id: int = 0, amount: float = 0, total_principal: float = 0, total_interest: float = 0, bal_principal: float = 0, bal_interest: float = 0, retrial_num: int = 0, status: int = 0, retrial_status: str = None, collected_at: str = None, commit: bool=False):
    collection = Collection(loan_id=loan_id, amount=amount, total_principal=total_principal, total_interest=total_interest, bal_principal=bal_principal, bal_interest=bal_interest, retrial_num=retrial_num, status=status, retrial_status=retrial_status, collected_at=collected_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(collection)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(collection)
    return collection

def update_collection(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Collection).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_collection(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Collection).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_collection(db: Session, id: int=0, commit: bool=False):
    db.query(Collection).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_collection_by_id(db: Session, id: int=0):
    return db.query(Collection).filter_by(id = id).first()

def get_collections_by_loan_id(db: Session, loan_id: int=0):
    return db.query(Collection).filter_by(loan_id = loan_id).order_by(desc(Collection.created_at)).all()

def get_collections(db: Session, filters: Dict={}):
    query = db.query(Collection)
    if 'loan_id' in filters:
        query = query.filter_by(loan_id = filters['loan_id'])
    if 'collected_at' in filters:
        query = query.filter_by(collected_at = filters['collected_at'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Collection.created_at))

def get_collections_by_collected_at(db: Session, collected_at: str=None):
    return db.query(Collection).filter(func.date(Collection.collected_at) == collected_at).all()

def count_collection_loan_id_collected_at(db: Session, loan_id: int=0, collected_at: str=None):
    return db.query(Collection).filter(and_(Collection.loan_id == loan_id, Collection.collected_at == collected_at)).count()

def sum_of_overdue_collections(db: Session):
    today_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(func.sum(Collection.amount)).filter(
        Collection.status == 0,
        Collection.collected_at < today_utc,
        Collection.deleted_at.is_(None)
    ).scalar() or 0.0

def count_collection_loan_id_status(db: Session, loan_id: int=0, status: int=0):
    return db.query(Collection).filter(and_(Collection.loan_id == loan_id, Collection.status == status)).count()

def get_total_principal_before_date(db: Session, before_date: str = None):
    if not before_date:
        return 0
    try:
        target_datetime = datetime.strptime(before_date, '%Y-%m-%d')
        
        result = db.query(func.coalesce(func.sum(Collection.total_principal), 0)).filter(
            Collection.collected_at < target_datetime,
            Collection.collected_at.isnot(None)
        ).scalar()
        
        return float(result) if result else 0.0
    
    except ValueError:
        return 0

def get_total_interest_before_date(db: Session, before_date: str = None):
    if not before_date:
        return 0
    try:
        target_datetime = datetime.strptime(before_date, '%Y-%m-%d')
        
        result = db.query(func.coalesce(func.sum(Collection.total_principal), 0)).filter(
            Collection.collected_at < target_datetime,
            Collection.collected_at.isnot(None)
        ).scalar()
        
        return float(result) if result else 0.0
    
    except ValueError:
        return 0