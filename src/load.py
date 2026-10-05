import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection


RAW_FILE = "data/raw/users.json"


def load_to_staging():
    print("Starting load to staging...")

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO staging_customers
            (
                customer_id,
                name,
                username,
                email,
                city,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for record in data:
            cursor.execute(
                insert_query,
                (
                    record["id"],
                    record["name"],
                    record["username"],
                    record["email"],
                    record["address"]["city"],
                    datetime.now()
                )
            )

        connection.commit()

        print("Data loaded successfully into staging_customers!")
        print(f"Records loaded: {len(data)}")

    except Exception as e:
        connection.rollback()
        print(f"Load failed: {e}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_to_staging()