import subprocess
import sys

PIPELINE_STEPS = [
    "src/ingestion/ingest_olist.py",

    "src/cleaning/products_cleaning.py",
    "src/cleaning/orders_cleaning.py",
    "src/cleaning/order_items_cleaning.py",
    "src/cleaning/payments_cleaning.py",

    "src/modeling/order_items_aggregation.py",
    "src/modeling/payments_aggregation.py",
    "src/modeling/fact_orders.py",
]

def run_pipeline():
    for step in PIPELINE_STEPS:
        print(f"\n▶ Running {step}")
        result = subprocess.run([sys.executable, step])

        if result.returncode != 0:
            raise RuntimeError(f"Pipeline failed at step: {step}")

    print("\n✅ Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()
