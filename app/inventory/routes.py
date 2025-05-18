from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.inventory.request import (
    SaleCreate,
    SalesFilter,
    RevenueAnalysis,
    RevenueComparison,
    InventoryResponse,
)
from app.inventory.response import SaleResponse, InventoryHistoryResponse
from app.inventory.services import (
    create_sale,
    get_sales,
    analyze_revenue,
    compare_revenue,
    get_inventory,
    update_inventory,
    get_inventory_history,
)
from config.database import get_db

router = APIRouter()


@router.post("/sales", response_model=SaleResponse)
def create_sale_endpoint(sale_data: SaleCreate, db: Session = Depends(get_db)):
    try:
        return create_sale(db, sale_data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sales", response_model=List[SaleResponse])
def get_sales_endpoint(filters: SalesFilter = Depends(), db: Session = Depends(get_db)):
    return get_sales(db, filters)


@router.get("/revenue/{period}", response_model=List[RevenueAnalysis])
def get_revenue_endpoint(
    period: str, category: str | None = None, db: Session = Depends(get_db)
):
    valid_periods = ["daily", "weekly", "monthly", "annual"]
    if period not in valid_periods:
        raise HTTPException(status_code=400, detail="Invalid period specified")
    return analyze_revenue(db, period, category)


@router.post("/revenue/comparison")
def compare_revenue_endpoint(
    comparison: RevenueComparison, db: Session = Depends(get_db)
):
    return compare_revenue(db, comparison)


@router.get("/inventory", response_model=List[InventoryResponse])
def get_inventory_endpoint(
    low_stock_threshold: int = 10, db: Session = Depends(get_db)
):
    return get_inventory(db, low_stock_threshold)


@router.put("/inventory/{product_id}", response_model=InventoryResponse)
def update_inventory_endpoint(
    product_id: int, new_quantity: int, db: Session = Depends(get_db)
):
    try:
        updated = update_inventory(db, product_id, new_quantity)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/inventory/history/{product_id}", response_model=List[InventoryHistoryResponse]
)
def get_inventory_history_endpoint(
    product_id: int, days: int = 30, db: Session = Depends(get_db)
):
    return get_inventory_history(db, product_id, days)
