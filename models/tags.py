from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Tag(Base):

    __tablename__ = "tags"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    products = relationship("Product", secondary="tags_products", back_populates="tags")

def create_tag(db: Session, merchant_id: int = 0, name: str = None, description: str = None, slug: str = None, status: int = 0, created_by: int = 0, commit: bool=False):
    tag = Tag(merchant_id=merchant_id, name=name, description=description, slug=slug, status=status, created_by=created_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(tag)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(tag)
    return tag

def update_tag(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Tag).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_tag(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Tag).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_tag(db: Session, id: int=0, commit: bool=False):
    db.query(Tag).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def count_tags(db: Session, filters: Dict={}):
    query = db.query(Tag)
    if 'name' in filters:
        query = query.filter_by(name = filters['name'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'created_by' in filters:
        query = query.filter_by(created_by = filters['created_by'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.count()

def count_tag_by_merchant_id_and_name(db: Session, merchant_id: int=0, name: str=None):
    return db.query(Tag).filter(and_(Tag.merchant_id == merchant_id, Tag.name == name)).count()

def get_single_tag_by_id(db: Session, id: int=0):
    return db.query(Tag).filter_by(id = id).first()

def get_single_tag_by_slug(db: Session, slug: str=None):
    return db.query(Tag).filter_by(slug = slug).first()

def get_single_tag_by_merchant_id_and_name(db: Session, merchant_id: int=0, name: str=None):
    return db.query(Tag).filter(and_(Tag.merchant_id == merchant_id, Tag.name == name)).first()

def get_tags(db: Session, filters: Dict={}):
    query = db.query(Tag)
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'created_by' in filters:
        query = query.filter_by(created_by = filters['created_by'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(Tag.name.like("%" + filters['name'] + "%"))
    if 'slug' in filters:
        query = query.filter(Tag.slug.like('%' + filters['slug'] + '%'))
    return query.order_by(desc(Tag.created_at))

def create_merchant_tag(db: Session, merchant_id: int=0, name: str=None, created_by: int=0, status: int=0, commit: bool=False):
    if count_tag_by_merchant_id_and_name(db=db, merchant_id=merchant_id, name=name) == 0:
        return create_tag(db=db, merchant_id=merchant_id, name=name, status=status, created_by=created_by, commit=commit)
    else:
        return get_single_tag_by_merchant_id_and_name(db=db, merchant_id=merchant_id, name=name)