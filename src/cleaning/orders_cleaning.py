from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def clean_orders(products_path: Path) -> pd.DataFrame:
    """
    Clean the raw products dataset.

    Parameters
    ----------
    products_path : Path
        Path to the raw products CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned products dataframe.
    """

    df = pd.read_csv(orders_path)

    # Check for missing columns in orders dataset
    expected_columns = {
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
      "order_estimated_delivery_date",
    }
    
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in products dataset: {missing_columns}")

    timestamp_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    # Remove rows with invalid timestamps
    for col in timestamp_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    
    valid_statuses = {"delivered"}
    # Remove rows with invalid order statuses (undelivered, canceled, etc.)

    df = df[df["order_status"].isin(valid_statuses)].copy()

    date_pairs = [
    ("order_purchase_timestamp", "order_approved_at"),
    ("order_approved_at", "order_delivered_carrier_date"),
    ("order_delivered_carrier_date", "order_delivered_customer_date"),
    ]
    # Remove rows with inconsistent/impossible date sequences

    invalid_date_mask = False

    for earlier, later in date_pairs:
        invalid_date_mask |= (
            df[earlier].notna() &
            df[later].notna() &
            (df[earlier] > df[later])
    )
        
    df = df.loc[~invalid_date_mask].copy()

    df["delivery_duration_days"] = df["order_delivered_customer_date"] - df["order_purchase_timestamp"]

    df["delivery_delay_days"] = df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]

    df["delivery_duration_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
    ).dt.days
    # Calculate delivery duration in days

    df["delivery_delay_days"] = (
    df["order_delivered_customer_date"]
    - df["order_estimated_delivery_date"]
    ).dt.days
    # Calculate delivery delay in days

    df = df[df["delivery_duration_days"] >= 0].copy()


    return df



if __name__ == "__main__":
    orders_path = RAW_DATA_DIR / "olist_orders_dataset.csv"

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df = clean_orders(orders_path)

    output_path = PROCESSED_DATA_DIR / "orders_cleaned.csv"
    cleaned_df.to_csv(output_path, index=False)
