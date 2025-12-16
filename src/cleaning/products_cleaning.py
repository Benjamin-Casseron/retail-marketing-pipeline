from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/olist")
PROCESSED_DATA_DIR = Path("data/processed/olist")

def clean_products(products_path: Path, category_translation_path: Path) -> pd.DataFrame:
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

    df = pd.read_csv(products_path)
    category_translation = pd.read_csv(category_translation_path)

    # Check for missing columns in category translation dataset
    expected_translation_columns = {
        "product_category_name",
        "product_category_name_english",
    }

    missing_translation_cols = expected_translation_columns - set(category_translation.columns)
    if missing_translation_cols:
        raise ValueError(
            f"Missing columns in category translation dataset: {missing_translation_cols}"
        )

    # Check for missing columns in products dataset
    expected_columns = {
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    }
    
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in products dataset: {missing_columns}")

    dimension_cols = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    ]
    
    # Remove rows with non-positive values in dimension columns
    invalid_mask = (
    (df[dimension_cols] <= 0) |
    (df[dimension_cols].isna())).any(axis=1)

    df = df.loc[~invalid_mask].copy()

    # Fill missing product category names with 'unknown'
    df["product_category_name"] = df["product_category_name"].fillna("unknown")

    metadata_cols = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    ]

    # Fill missing metadata columns with 0
    df[metadata_cols] = df[metadata_cols].fillna(0)

    # Merge with category translation to get English names
    df = df.merge(
    category_translation,
    on="product_category_name",
    how="left"
    )
    # Fill missing English category names with 'unknown'
    df["product_category_name_english"] = (
        df["product_category_name_english"]
        .fillna("unknown")
    )
    return df

if __name__ == "__main__":
    products_path = RAW_DATA_DIR / "olist_products_dataset.csv"
    category_translation_path = RAW_DATA_DIR / "product_category_name_translation.csv"

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df = clean_products(
        products_path=products_path,
        category_translation_path=category_translation_path,
    )

    output_path = PROCESSED_DATA_DIR / "products_cleaned.csv"
    cleaned_df.to_csv(output_path, index=False)
