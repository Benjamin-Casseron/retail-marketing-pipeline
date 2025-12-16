# Retail Marketing Analytics Pipeline (Olist)

## Overview

This project implements a complete, reproducible analytics pipeline using the **Olist Brazilian e-commerce dataset**.

The objective is to transform raw transactional data into a **business-ready order-level fact table**, suitable for BI tools (Power BI, Tableau) and analytical use cases such as marketing performance, order-level customer segmentation, and delivery operations.

The project follows **analytics engineering best practices**:
- clear separation of raw, cleaned, and modeled data
- explicit data validation and cleaning rules
- deterministic, script-based transformations
- well-defined data grain and metrics
- strong documentation and reproducibility

---

## Current Status
✅ Data ingestion pipeline implemented  
✅ Raw data schema fully inspected and documented  
✅ Product-level cleaning and normalization  
✅ Orders cleaning with delivery duration and delay metrics  
✅ Order items cleaning and aggregation  
✅ Payments cleaning and aggregation  
✅ Fact orders table modeled at order granularity  
✅ Customers dimension cleaned for BI slicing  
⏳ Power BI dashboarding (in progress)


## Data Source

- **Olist Brazilian E-commerce Dataset**
- Public dataset available on Kaggle
- Programmatically ingested using the Kaggle API

---

## Project Structure

```text
retail-marketing-pipeline/
├── data/
│   ├── raw/                # Raw data (not committed)
│   ├── processed/          # Cleaned datasets (not committed)
│   └── modeled/            # Aggregated / fact tables (not committed)
├── notebooks/
│   └── 01_schema_inspection.ipynb
├── src/
│   ├── ingestion/
│   │   └── ingest_olist.py
│   ├── cleaning/
│   │   ├── customers_cleaning.py
│   │   ├── orders_cleaning.py
│   │   ├── products_cleaning.py
│   │   ├── payments_cleaning.py
│   │   └── order_items_cleaning.py
│   └── modeling/
│       ├── order_items_aggregation.py
│       ├── payments_aggregation.py
│       └── fact_orders.py
├── powerbi/
│   └── retail_marketing_report.pbix   # Power BI report (not committed)
├── requirements.txt
└── README.md

```

---

## Pipeline Stages

### 1. Ingestion
- Automated download of the dataset via Kaggle CLI
- Idempotent script (safe to re-run)
- No manual intervention required

### 2. Cleaning (Row-Level)
Each raw table is cleaned independently with explicit rules:
- schema validation (expected columns)
- data type normalization
- removal of invalid or inconsistent records
- business-aware handling of edge cases (free items, vouchers, undefined payment types)

Outputs are stored in `data/processed/olist/`.

### 3. Modeling (Analytical Layer)
Cleaned tables are aggregated and joined to produce analytical datasets:
- order items aggregated to order level
- payments aggregated to order level
- construction of a **single fact table** with one row per order

Outputs are stored in `data/modeled/olist/`.

---

## Final Output: Fact Orders Table

## Power BI
The Power BI report (`.pbix`) is not committed to version control.
PBIX files are binary and environment-specific.  
The report can be rebuilt by loading the modeled CSV files from `data/modeled/`.

**File**
data/modeled/olist/fact_orders.csv

**Grain**
- One row per `order_id`

**Key Metrics**
- `order_items_count`
- `order_items_total_value`
- `order_freight_total`
- `order_payment_total`
- `payment_methods_count`
- `used_voucher` (boolean indicator)

**Delivery Metrics**
- `delivery_duration_days`
- `delivery_delay_days`

This table is designed for **direct consumption in Power BI** or SQL-based analytics workflows.


### Run the Full Pipeline

To execute the entire pipeline end-to-end:

```bash
python src/run_pipeline.py

```

---

## Skills Demonstrated :

- Python (pandas, pathlib)
- Data cleaning and validation
- Analytics engineering principles
- Fact table design and grain control
- Reproducible data pipelines
- BI-oriented data modeling

## Next Steps :

- Dimensional modeling (customers, products, sellers)
- Power BI dashboarding and KPI design
- Marketing, retention, and delivery performance analysis