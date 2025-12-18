from pathlib import Path
import pandas as pd

PROCESSED_DATA_DIR = Path("data/processed/olist")
MODELED_DATA_DIR = Path("data/modeled/olist")

def payments_aggregation(df : pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate payments data to get total payment value and number of payments per order.

    Returns
    -------
    pd.DataFrame
        Aggregated payments dataframe with total_payment_value and payment_count per order_id.
    """
    agg_df = (
    df.groupby("order_id")
      .agg(
          order_payment_total=("payment_value", "sum"),
          payment_methods_count=("payment_type", "count"),
          used_voucher=("payment_type", lambda x: "voucher" in x.values),
      )
      .reset_index()
    )


    return agg_df

if __name__ == "__main__":
    payments_path = PROCESSED_DATA_DIR / "payments_cleaned.csv"
    MODELED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    agg_df = pd.read_csv(payments_path)
    agg_df = payments_aggregation(agg_df)

    
    output_path = MODELED_DATA_DIR / "payments_aggregated.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    agg_df.to_csv(output_path, index=False)