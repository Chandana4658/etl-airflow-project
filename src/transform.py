import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection


def incremental_load():
    print("Starting incremental load...")

    connection = get_connection()
    cursor = connection.cursor()

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

        connection.commit()

        print("Incremental load completed successfully!")
        print(f"Records inserted/updated: {cursor.rowcount}")

    except Exception as e:
        connection.rollback()
        print(f"Incremental load failed: {e}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    incremental_load()