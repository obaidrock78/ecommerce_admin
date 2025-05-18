from datetime import datetime, timedelta

from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.inventory.models import Inventory, Sale, Product, InventoryHistory
from app.inventory.request import SalesFilter, RevenueComparison


def create_sale(db: Session, sale_data: dict):
    db_sale = Sale(**sale_data)

    # Update inventory
    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == sale_data["product_id"])
        .first()
    )
    if inventory:
        inventory.current_quantity -= sale_data["quantity"]

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sales(db: Session, filters: SalesFilter):
    query = db.query(Sale)

    if filters.start_date:
        query = query.filter(Sale.sale_date >= filters.start_date)
    if filters.end_date:
        query = query.filter(Sale.sale_date <= filters.end_date)
    if filters.product_id:
        query = query.filter(Sale.product_id == filters.product_id)
    if filters.category:
        query = query.join(Product).filter(Product.category == filters.category)

    return query.all()


def analyze_revenue(db: Session, period: str, category: str | None):
    date_formats = {
        "daily": "%Y-%m-%d",
        "weekly": "%Y-%u",
        "monthly": "%Y-%m",
        "annual": "%Y",
    }

    query = db.query(
        func.strftime(date_formats[period], Sale.sale_date).label("period"),
        func.sum(Sale.total_price).label("total_revenue"),
        Product.category if category else None,
    ).join(Product)

    if category:
        query = query.filter(Product.category == category)
        query = query.group_by("period", Product.category)
    else:
        query = query.group_by("period")

    return query.all()


def compare_revenue(db: Session, comp_data: RevenueComparison):
    # First period calculation
    period1 = db.query(func.sum(Sale.total_price)).filter(
        Sale.sale_date.between(comp_data.period1_start, comp_data.period1_end)
    )

    # Second period calculation
    period2 = db.query(func.sum(Sale.total_price)).filter(
        Sale.sale_date.between(comp_data.period2_start, comp_data.period2_end)
    )

    if comp_data.category:
        period1 = period1.join(Product).filter(Product.category == comp_data.category)
        period2 = period2.join(Product).filter(Product.category == comp_data.category)

    p1_total = period1.scalar() or 0
    p2_total = period2.scalar() or 0

    return {
        "period1_total": p1_total,
        "period2_total": p2_total,
        "difference": p2_total - p1_total,
        "percentage_change": (
            ((p2_total - p1_total) / p1_total * 100) if p1_total != 0 else 0
        ),
    }


def get_inventory(db: Session, low_stock_threshold: int = 10):
    return (
        db.query(
            Inventory.product_id,
            Product.name.label("product_name"),
            Product.category,
            Inventory.current_quantity,
            Inventory.last_updated,
            case(
                (Inventory.current_quantity < low_stock_threshold, True), else_=False
            ).label("low_stock"),
        )
        .join(Product)
        .all()
    )


def update_inventory(db: Session, product_id: int, new_quantity: int):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise ValueError("Product not found in inventory")

    history = InventoryHistory(
        product_id=product_id,
        old_quantity=inventory.current_quantity,
        new_quantity=new_quantity,
    )
    inventory.current_quantity = new_quantity
    db.add(history)
    db.commit()
    return inventory


def get_inventory_history(db: Session, product_id: int, days: int = 30):
    start_date = datetime.now() - timedelta(days=days)
    return (
        db.query(InventoryHistory)
        .filter(
            InventoryHistory.product_id == product_id,
            InventoryHistory.change_date >= start_date,
        )
        .order_by(InventoryHistory.change_date.desc())
        .all()
    )
