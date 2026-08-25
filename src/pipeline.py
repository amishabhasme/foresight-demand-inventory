from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_data():
    """Load the Week 1 raw datasets."""
    sales = pd.read_csv(RAW_DIR / "sales_daily.csv")
    inventory = pd.read_csv(RAW_DIR / "inventory_snapshots.csv")

    return sales, inventory


def clean_data(sales, inventory):
    """Apply the Week 1 cleaning required for downstream analysis."""

    # Standardize column names
    sales.columns = sales.columns.str.strip()
    inventory.columns = inventory.columns.str.strip()

    # Remove completely empty rows
    sales = sales.dropna(how="all")
    inventory = inventory.dropna(how="all")

    return sales, inventory


def save_processed_data(sales, inventory):
    """Save cleaned datasets for downstream analysis."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    sales.to_csv(
        PROCESSED_DIR / "sales_clean.csv",
        index=False
    )

    inventory.to_csv(
        PROCESSED_DIR / "inventory_clean.csv",
        index=False
    )


def main():
    sales, inventory = load_data()

    print("Raw Sales:", sales.shape)
    print("Raw Inventory:", inventory.shape)

    sales_clean, inventory_clean = clean_data(
        sales,
        inventory
    )

    save_processed_data(
        sales_clean,
        inventory_clean
    )

    print("Processed Sales:", sales_clean.shape)
    print("Processed Inventory:", inventory_clean.shape)

    print("\nPipeline completed successfully.")
    print(f"Output: {PROCESSED_DIR / 'sales_clean.csv'}")
    print(f"Output: {PROCESSED_DIR / 'inventory_clean.csv'}")


if __name__ == "__main__":
    main()