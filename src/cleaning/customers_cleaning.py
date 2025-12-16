from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def clean_customers(customers_path: Path) -> pd.DataFrame:
    """
    Cleans customer data by handling missing values, and standardizing formats.

    Parameters:
    - customers_path : Path to the input CSV file containing raw customer data.

    Returns:
    - pd.DataFrame : Cleaned customer data.
    """
    # Load the data
    df = pd.read_csv(customers_path)

    expected_columns = {
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    }

    # Check for missing columns in customers dataset
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in customers dataset: {missing_columns}")
    
    # Ensure customer_id uniqueness (assertion)
    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer_id values found in customers dataset.")

    # Standardize text formats
    df["customer_city"] = df["customer_city"].astype(str).str.lower().str.strip()
    df["customer_state"] = df["customer_state"].astype(str).str.upper().str.strip()


    return df

if __name__ == "__main__":
    customers_path = RAW_DATA_DIR / "olist_customers_dataset.csv"
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df = clean_customers(customers_path)
    output_path = PROCESSED_DATA_DIR / "customers_cleaned.csv"

    cleaned_df.to_csv(output_path, index=False)