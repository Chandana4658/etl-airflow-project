import os
import sys
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection


def incremental_load():
    print("Starting incremental load...")

    run_id = str(uuid.uuid4())
    pipeline_name = "customer_etl_pipeline"
    start_time = datetime.now()

    connection = get_connection()
    cursor = connection.cursor()

    records_processed = 0
    status = "SUCCESS"
    error_message = None

    try:
        upsert_query = """
            INSERT INTO customers (
                customer_id,
                name,
                username,
                email,
                city,
                updated_at
            )
            SELECT
                customer_id,
                name,
                username,
                email,
                city,
                updated_at
            FROM staging_customers
            ON CONFLICT (customer_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                username = EXCLUDED.username,
                email = EXCLUDED.email,
                city = EXCLUDED.city,
                updated_at = EXCLUDED.updated_at;
        """

        cursor.execute(upsert_query)

        records_processed = cursor.rowcount

        connection.commit()

        print("Incremental load completed successfully!")
        print(f"Records processed: {records_processed}")

    except Exception as e:
        connection.rollback()

        status = "FAILED"
        error_message = str(e)

        print(f"Incremental load failed: {error_message}")

        raise

    finally:
        end_time = datetime.now()

        audit_query = """
            INSERT INTO pipeline_audit (
                run_id,
                pipeline_name,
                start_time,
                end_time,
                records_processed,
                status,
                error_message
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            audit_query,
            (
                run_id,
                pipeline_name,
                start_time,
                end_time,
                records_processed,
                status,
                error_message
            )
        )

        connection.commit()

        cursor.close()
        connection.close()


if __name__ == "__main__":
    incremental_load()