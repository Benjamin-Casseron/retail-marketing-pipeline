# Retail Marketing Data Pipeline (Olist Dataset)

## Project Overview
This project is an end-to-end data pipeline built on the Brazilian Olist e-commerce dataset.
The goal is to demonstrate professional data analysis practices, from raw data ingestion
to cleaned, analysis-ready datasets and downstream analytics.

The project emphasizes:
- Reproducible pipelines
- Clear data modeling
- Proper separation between exploration and production code
- Strong documentation

## Current Status
✅ Data ingestion pipeline implemented  
✅ Raw data schema fully inspected and documented  
✅ Product-level cleaning and normalization 
✅ Orders cleaning with delivery duration and delay metrics 
✅ Order_items cleaning (row level hygiene)
⏳ Data cleaning pipeline (in progress) 
⏳ Analytical modeling and dashboarding (planned)

## Project Structure
```text
retail-marketing-pipeline/
├── data/
│   ├── raw/           # Raw data (not committed)
│   └── processed/     # Cleaned data outputs (not committed)
├── notebooks/
│   └── 01_schema_inspection.ipynb
├── src/
│   ├── ingestion/
│   │   └── ingest_olist.py
│   └── cleaning/      # Cleaning logic (to be implemented)
├── requirements.txt
└── README.md
```

Dataset

The project uses the public Olist Brazilian E-commerce dataset available on Kaggle.
Next Steps

    Implement table-by-table cleaning functions

    Build a unified analytical dataset

    Perform exploratory analysis

    Create a business-oriented dashboard