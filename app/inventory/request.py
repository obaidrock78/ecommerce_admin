from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_date: date
    total_price: float = Field(..., gt=0)


class SaleCreate(SaleBase):
    pass


class InventoryBase(BaseModel):
    current_quantity: int = Field(..., ge=0)


class InventoryUpdate(InventoryBase):
    pass


class RevenueComparison(BaseModel):
    period1_start: date
    period1_end: date
    period2_start: date
    period2_end: date
    category: Optional[str] = None


class SalesFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    product_id: Optional[int] = None
    category: Optional[str] = None


class InventoryResponse(InventoryBase):
    product_id: int
    product_name: str
    category: str
    last_updated: datetime
    low_stock: bool


class RevenueAnalysis(BaseModel):
    period: str
    total_revenue: float
    category: Optional[str] = None
