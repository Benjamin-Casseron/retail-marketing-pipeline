from pathlib import Path
import pandas as pd

PROCESSED_DATA_DIR = Path("data/processed/olist")
MODELED_DATA_DIR = Path("data/modeled/olist")

def fact_orders(orders_df: pd.DataFrame, order_items_df: pd.DataFrame, payments_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a fact orders dataframe by merging orders, order items aggregation, and payments aggregation data.

    Returns
    -------
    pd.DataFrame
        Merged fact orders dataframe.
    """
    fact_df = orders_df.merge(order_items_df, on="order_id", how="left")
    fact_df = fact_df.merge(payments_df, on="order_id", how="left")

    numeric_fill_zero = [
    "order_items_count",
    "order_items_total_value",
    "order_freight_total",
    "order_payment_total",
    "payment_methods_count",
    ]
    fact_df[numeric_fill_zero] = fact_df[numeric_fill_zero].fillna(0)
    # Fill NaN values in numeric columns with 0

    fact_df["used_voucher"] = (
    fact_df["used_voucher"]
    .astype("boolean")
    .fillna(False)
    )




    # Convert used_voucher to boolean

    fact_df["order_items_count"] = fact_df["order_items_count"].astype(int)
    fact_df["payment_methods_count"] = fact_df["payment_methods_count"].astype(int)
    # Enforcing correct data types

    fact_df["order_purchase_timestamp"] = pd.to_datetime(
    fact_df["order_purchase_timestamp"], errors="coerce"
    )
    # Ensure order_purchase_timestamp is in datetime format

    final_columns = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "delivery_duration_days",
    "delivery_delay_days",
    "order_items_count",
    "order_items_total_value",
    "order_freight_total",
    "order_payment_total",
    "payment_methods_count",
    "used_voucher",
    ]

    fact_df = fact_df[final_columns]

    return fact_df

if __name__ == "__main__":
    orders_path = PROCESSED_DATA_DIR / "orders_cleaned.csv"
    orders_df = pd.read_csv(orders_path)

    order_items_path = MODELED_DATA_DIR / "order_items_aggregated.csv"
    order_items_df = pd.read_csv(order_items_path)

    payments_path = MODELED_DATA_DIR / "payments_aggregated.csv"
    payments_df = pd.read_csv(payments_path)

    fact_df = fact_orders(
    orders_df=orders_df,
    order_items_df=order_items_df,
    payments_df=payments_df
    )
    MODELED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = MODELED_DATA_DIR / "fact_orders.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fact_df.to_csv(output_path, index=False)

