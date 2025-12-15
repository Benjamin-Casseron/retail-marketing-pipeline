from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def clean_payments(payments_path: Path):
    """
    Clean the raw payments dataset.

    Parameters
    ----------
    payments_path : Path
        Path to the raw payments CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned payments dataframe.
    """

    df = pd.read_csv(payments_path)

    # Check for missing columns in payments dataset
    expected_columns = {
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    }
    
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in payments dataset: {missing_columns}")

    # Remove rows with negative payment values
    df = df[df["payment_value"] >= 0].copy()

    # Remove negative installments, keep 0 installments (some orders might be paid in full without installments)
    df = df[df["payment_installments"] >= 0].copy()

    # Normalize payment_type values to lowercase and strip whitespace
    df["payment_type"] = df["payment_type"].str.strip().str.lower()

    # Replace 'not_defined' payment types with NaN
    df.loc[df["payment_type"] == "not_defined", "payment_type"] = pd.NA



    return df

if __name__ == "__main__":
    payments_path = RAW_DATA_DIR / "olist_order_payments_dataset.csv"

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df = clean_payments(payments_path)

    output_path = PROCESSED_DATA_DIR / "payments_cleaned.csv"
    cleaned_df.to_csv(output_path, index=False)