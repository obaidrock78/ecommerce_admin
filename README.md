# E-commerce Admin API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Backend API for e-commerce management system with sales analytics and inventory management capabilities.

## Features
- Sales tracking with date/product filters
- Multi-period revenue analysis (daily/weekly/monthly/annual)
- Inventory management with stock history tracking
- Low stock alerts with configurable thresholds
- JWT Authentication
- PostgreSQL database with Alembic migrations

## API Endpoints

### Sales Management
| Method | Endpoint | Parameters | Description |
|--------|----------|------------|-------------|
| POST | `/sales` | `product_id`, `quantity`, `sale_date` | Record new sale |
| GET | `/sales` | `start_date`, `end_date`, `category` | Get filtered sales records |

### Revenue Analysis
| Method | Endpoint | Parameters | Description |
|--------|----------|------------|-------------|
| GET | `/revenue/{period}` | `period`, `category` | Get revenue breakdown by time period |
| POST | `/revenue/comparison` | `base_period`, `compare_period` | Compare revenue between periods |

### Inventory Management
| Method | Endpoint | Parameters | Description |
|--------|----------|------------|-------------|
| GET | `/inventory` | `low_stock_threshold` | List current inventory status |
| PUT | `/inventory/{product_id}` | `new_quantity` | Update product stock quantity |
| GET | `/inventory/history/{product_id}` | `days` (default: 30) | Get inventory change history |

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Pip package manager

```bash
# Clone repository
git clone https://github.com/obaidrock78/ecommerce_admin/
cd ecommerce-admin

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
