import os
import sys

# Allow Python to find modules inside src/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract_data
from validate import validate_data
from load import load_to_staging
from transform import incremental_load


def run_pipeline():
    print("=" * 60)
    print("STARTING CUSTOMER ETL PIPELINE")
    print("=" * 60)

    print("\n[1] EXTRACT")
    extract_data()

    print("\n[2] VALIDATE")
    validate_data()

    print("\n[3] LOAD TO STAGING")
    load_to_staging()

    print("\n[4] INCREMENTAL LOAD")
    incremental_load()

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()