from pathlib import Path
import pandas as pd

MODELED_DATA_DIR = Path("data/modeled/olist")
def build_date_dimension(fact_orders_path: Path) -> pd.DataFrame:

    """
    Build a date dimension based on order_purchase_timestamp
    from the fact_orders table.

    Parameters
    ----------
    fact_orders_path : Path
        Path to the fact_orders CSV file.

    Returns
    -------
    pd.DataFrame
        Date dimension dataframe (one row per calendar day).
    """
    # Load fact_orders to determine date range
    df = pd.read_csv(fact_orders_path)
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )

    # Determine date range from fact_orders
    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()

    # Create date range
    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    date_dim = pd.DataFrame({"date": date_range})

    


    # Extract date components
    date_dim["day"] = date_dim["date"].dt.day
    date_dim["day_name"] = date_dim["date"].dt.day_name()
    date_dim["month"] = date_dim["date"].dt.month
    date_dim["month_name"] = date_dim["date"].dt.month_name()
    date_dim["year"] = date_dim["date"].dt.year
    date_dim["year_month"] = date_dim["date"].dt.to_period("M").astype(str)
    date_dim["day_of_week"] = date_dim["date"].dt.dayofweek + 1  # Monday=1, Sunday=7
    date_dim["is_weekend"] = date_dim["day_of_week"].isin([6, 7])

    # Convert to date only (no time component)
    date_dim["date"] = date_dim["date"].dt.date

    return date_dim

if __name__ == "__main__":
    fact_orders_path = MODELED_DATA_DIR / "fact_orders.csv"

    MODELED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    date_dim_df = build_date_dimension(fact_orders_path)

    output_path = MODELED_DATA_DIR / "dim_date.csv"
    date_dim_df.to_csv(output_path, index=False)