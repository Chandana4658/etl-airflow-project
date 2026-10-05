import json
import os

import requests


API_URL = "https://jsonplaceholder.typicode.com/users"
RAW_DIR = "data/raw"
RAW_FILE = os.path.join(RAW_DIR, "users.json")


def extract_data():
    print("Starting data extraction...")

    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    data = response.json()

    os.makedirs(RAW_DIR, exist_ok=True)

    with open(RAW_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Extraction successful!")
    print(f"Records extracted: {len(data)}")
    print(f"Raw data saved to: {RAW_FILE}")

    return data


if __name__ == "__main__":
    extract_data()