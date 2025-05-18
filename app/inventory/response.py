from datetime import date, datetime

from pydantic import BaseModel, Field


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_date: date
    total_price: float = Field(..., gt=0)


class SaleResponse(SaleBase):
    id: int

    class Config:
        orm_mode = True


class InventoryHistoryResponse(BaseModel):
    old_quantity: int
    new_quantity: int
    change_date: datetime

    class Config:
        orm_mode = True
