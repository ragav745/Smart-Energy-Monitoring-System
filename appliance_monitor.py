
import csv
import os

FILE_NAME = "appliances.csv"

class Appliance:
    def __init__(self, name, power, hours):
        self.name = name
        self.power = power
        self.hours = hours

    def calculate_energy(self):
        return (self.power * self.hours) / 1000


def load_appliances():
    appliances = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                appliance = Appliance(
                    row["Name"],
                    float(row["Power"]),
                    float(row["Hours"])
                )
                appliances.append(appliance)

    return appliances


def save_appliances(appliances):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Power", "Hours"])

        for appliance in appliances:
            writer.writerow([
                appliance.name,
                appliance.power,
                appliance.hours
            ])


def add_appliance():
    try:
        name = input("Enter appliance name: ").strip()
        power = float(input("Enter power (W): "))
        hours = float(input("Enter usage hours: "))

        if not name or power <= 0 or hours <= 0:
            print("Invalid details! Values must be positive.")
            return

        appliances = load_appliances()
        appliances.append(Appliance(name, power, hours))
        save_appliances(appliances)

        print("Appliance added successfully!")

    except ValueError:
        print("Please enter valid numbers!")


def view_appliances():
    appliances = load_appliances()

    if not appliances:
        print("No appliances found.")
        return

    print("\n----- APPLIANCE LIST -----")

    for i, appliance in enumerate(appliances, start=1):
        energy = appliance.calculate_energy()

        print(
            i, appliance.name,
            "| Power:", appliance.power, "W",
            "| Hours:", appliance.hours,
            "| Energy:", round(energy, 2), "kWh"
        )


def update_appliance():
    appliances = load_appliances()
    view_appliances()

    if not appliances:
        return

    try:
        number = int(input("Enter appliance number to update: "))

        if number < 1 or number > len(appliances):
            print("Invalid appliance number!")
            return

        name = input("Enter new name: ").strip()
        power = float(input("Enter new power (W): "))
        hours = float(input("Enter new usage hours: "))

        if not name or power <= 0 or hours <= 0:
            print("Invalid details! Nothing was updated.")
            return

        appliances[number - 1] = Appliance(name, power, hours)
        save_appliances(appliances)

        print("Appliance updated successfully!")

    except ValueError:
        print("Please enter valid input!")


def delete_appliance():
    appliances = load_appliances()
    view_appliances()

    if not appliances:
        return

    try:
        number = int(input("Enter appliance number to delete: "))

        if number < 1 or number > len(appliances):
            print("Invalid appliance number!")
            return

        removed = appliances.pop(number - 1)
        save_appliances(appliances)

        print(removed.name, "deleted successfully!")

    except ValueError:
        print("Please enter a valid number!")


def main():
    while True:
        print("\n===== SMART ENERGY MONITORING =====")
        print("1. Add Appliance")
        print("2. View Appliances")
        print("3. Update Appliance")
        print("4. Delete Appliance")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_appliance()
        elif choice == "2":
            view_appliances()
        elif choice == "3":
            update_appliance()
        elif choice == "4":
            delete_appliance()
        elif choice == "5":
            print("Thank you!")
            break
        else:
            print("Invalid choice! Select 1 to 5.")


if __name__ == "__main__":
    main()
