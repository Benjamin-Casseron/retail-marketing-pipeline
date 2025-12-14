import os
import subprocess
from pathlib import Path

def download_olist_dataset(download_dir: str):


    """
    Download the Olist dataset using the Kaggle API.

    Parameters
    ----------
    download_dir : str
        Path to the directory where the dataset will be saved.

    Notes
    -----
    This function wraps the Kaggle CLI. It ensures directories exist,
    avoids re-downloading if files are already present, and handles errors
    in a controlled manner.
    """


    download_path = Path(download_dir)
    # Create directory if it doesn't exist
    if not download_path.exists():
        download_path.mkdir(parents=True, exist_ok=True)


    # Check if dataset already exists
    existing_files = list(download_path.glob('*.csv'))
    if existing_files:
        print(f"Dataset already exists in {download_dir}. Skipping download.")
        return

    # Construct the Kaggle "download" command
    kaggle_command = [
        'kaggle',
        'datasets',
        'download',
        '-d',
        'olistbr/brazilian-ecommerce',
        '-p',
        str(download_path),
        '--unzip'
    ]

    # Execute the command
    result = subprocess.run(
        kaggle_command,
        capture_output=True,
        text=True
    )

    # Check for errors
    if result.returncode != 0:
        print("Error downloading dataset:")
        print(result.stderr)
        raise RuntimeError("Kaggle dataset download failed.")
    else:
        print(f"Dataset downloaded successfully to {download_dir}.")

        # At this point, download succeeded. Let's inspect folder structure.

        # 1. Check if CSVs are already at the top level (most likely case)
        top_level_csvs = list(download_path.glob("*.csv"))
        if top_level_csvs:
            print("Top-level CSV structure is already correct. ingest_olist complete")
            return

        # 2. If no CSVs at top level, look for a nested folder
        subdirs = [p for p in download_path.iterdir() if p.is_dir()]
        if not subdirs:
            # No CSVs and no subdirectories = unexpected layout
            raise RuntimeError(
                f"No CSV files found in {download_path} and no nested folders to inspect."
            )

        nested_folder = subdirs[0]

        # 3. Move CSVs from nested folder to top level
        for file in nested_folder.glob("*.csv"):
            file.rename(download_path / file.name)

        # 4. Try to remove the now-empty nested folder
        try:
            nested_folder.rmdir()
        except OSError:
            # If folder isn't empty, we ignore it; it doesn't affect CSV availability
            pass

        print("Nested folder structure normalized. ingest_olist complete.")

if __name__ == "__main__":
    target_dir = "data/raw/olist"
    download_olist_dataset(target_dir)



