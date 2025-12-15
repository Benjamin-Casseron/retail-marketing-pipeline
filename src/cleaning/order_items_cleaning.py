from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def clean_order_items(order_items_path: Path) -> pd.DataFrame:
    """
    Clean the raw order_items dataset.

    Parameters
    ----------
    order_items_path : Path
        Path to the raw order_items CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned order_items dataframe.
    """

    df = pd.read_csv(order_items_path)

    # Check for missing columns in order_items dataset
    expected_columns = {
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
}
    
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in order_items dataset: {missing_columns}")

    # Remove rows with negative prices or freight values, keep 0 values (free items/shipping promotions)
    df = df[(df["price"] >= 0) & (df["freight_value"] >= 0)].copy()

    # Convert shipping_limit_date to datetime
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

    return df

if __name__ == "__main__":
    order_items_path = RAW_DATA_DIR / "olist_order_items_dataset.csv"

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df = clean_order_items(order_items_path)

    output_path = PROCESSED_DATA_DIR / "order_items_cleaned.csv"
    cleaned_df.to_csv(output_path, index=False)