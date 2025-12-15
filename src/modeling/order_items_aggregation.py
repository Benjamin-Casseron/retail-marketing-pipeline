from pathlib import Path
import pandas as pd

MODELED_DATA_DIR = Path("data/modeled/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def order_items_aggregation(df : pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate order items data to get total items and total value per order.

    Returns
    -------
    pd.DataFrame
        Aggregated order items dataframe with total_items, total_value and freight value per order_id.
    """
    agg_df = df.groupby("order_id").agg(
        order_items_count=pd.NamedAgg(column="order_item_id", aggfunc="count"),
        order_items_total_value=pd.NamedAgg(column="price", aggfunc="sum"),
        order_freight_total=pd.NamedAgg(column="freight_value", aggfunc="sum"),
    ).reset_index()

    return agg_df

if __name__ == "__main__":
    order_item_path = PROCESSED_DATA_DIR / "order_items_cleaned.csv"

    agg_df = pd.read_csv(order_item_path)
    agg_df = order_items_aggregation(agg_df)
    
    output_path = MODELED_DATA_DIR / "order_items_aggregated.csv"
    agg_df.to_csv(output_path, index=False)