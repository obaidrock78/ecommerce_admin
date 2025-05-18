from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.baselayer.basemodel import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    sales = relationship('Sale', back_populates='product', cascade='all, delete-orphan')
    inventory = relationship('Inventory', uselist=False, back_populates='product', cascade='all, delete-orphan')


class Sale(BaseModel):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False, index=True)
    total_price = Column(Float, nullable=False)
    product = relationship('Product', back_populates='sales')


class Inventory(BaseModel):
    __tablename__ = "inventory"

    # Use BaseModel id as primary key; enforce each product appears once via unique constraint
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, unique=True, index=True)
    current_quantity = Column(Integer, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    product = relationship('Product', back_populates='inventory')
    history = relationship('InventoryHistory', back_populates='inventory', cascade='all, delete-orphan')


class InventoryHistory(BaseModel):
    __tablename__ = "inventory_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('inventory.product_id'), nullable=False, index=True)
    old_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    change_date = Column(DateTime, server_default=func.now(), nullable=False)

    inventory = relationship('Inventory', back_populates='history')
