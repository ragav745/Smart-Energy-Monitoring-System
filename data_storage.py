
import csv
import os
from datetime import datetime

FILE_NAME = "energy_data.csv"

FIELDS = [
    "Date", "Appliance", "V", "Current", "Power",
    "Hours", "Energy_kWh", "Tariff", "Bill_Rs"
]


def save_reading(appliance, voltage, current, power,
                 hours, energy, tariff, bill):

    rows = []

    # Read existing records so older data is preserved
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for old_row in reader:
                rows.append({
                    field: old_row.get(field, "")
                    for field in FIELDS
                })

    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Appliance": appliance,
        "V": voltage,
        "Current": current,
        "Power": power,
        "Hours": hours,
        "Energy_kWh": energy,
        "Tariff": tariff,
        "Bill_Rs": bill
    }

    rows.append(new_row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print("Reading saved successfully!")
