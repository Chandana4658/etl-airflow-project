import json
import os
import re


RAW_FILE = "data/raw/users.json"


def validate_data():
    print("Starting data validation...")

    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f"File not found: {RAW_FILE}")

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Expected API data to be a list")

    required_fields = ["id", "name", "username", "email", "address"]

    for record in data:

        # Check required fields
        for field in required_fields:
            if field not in record:
                raise ValueError(
                    f"Missing required field '{field}'"
                )

        # Check customer ID
        if record["id"] is None:
            raise ValueError("Customer ID cannot be NULL")

        # Check name
        if not record["name"]:
            raise ValueError("Customer name cannot be empty")

        # Check email
        if not record["email"]:
            raise ValueError("Customer email cannot be empty")

        # Basic email validation
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, record["email"]):
            raise ValueError(
                f"Invalid email: {record['email']}"
            )

    # Check duplicate IDs
    ids = [record["id"] for record in data]

    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate customer IDs found")

    print("Data validation successful!")
    print(f"Records validated: {len(data)}")

    return data


if __name__ == "__main__":
    validate_data()