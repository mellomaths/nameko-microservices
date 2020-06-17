import datetime

from sqlalchemy import (
    DECIMAL, Column, DateTime, ForeignKey, Integer, Table, String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)

product_ordered_association_table = Table('association', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


class Order(DeclarativeBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    products = relationship('ProductOrdered', secondary=product_ordered_association_table)


class ProductOrdered(DeclarativeBase):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    order = relationship(Order, backref="product")
    product_id = Column(Integer, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    # id = fields.String(dump_only=True)
    # title = fields.String(required=True, validate=must_not_be_blank)
    # description = fields.String(required=True, validate=must_not_be_blank)
    # department = fields.String(required=True, validate=must_not_be_blank)
    # price = fields.Float(required=True)
    # quantity = fields.Integer(required=True)
    # created_at = fields.DateTime(dump_only=True)
