
import csv
import os
from datetime import datetime

file_name = "energy_data.csv"

# Check whether CSV file already exists
file_exists = os.path.exists(file_name)

# Get appliance details
name = input("Enter appliance name: ")
power = float(input("Enter power (W): "))
hours = float(input("Enter daily usage (hours): "))

energy = (power * hours) / 1000

# Save readings
with open(file_name, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists or os.path.getsize(file_name) == 0:
        writer.writerow(["Date", "Appliance", "Power", "Hours", "Energy"])

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        name,
        power,
        hours,
        energy
    ])

print("Energy reading saved successfully!")
print("Energy Consumption:", energy, "kWh")
