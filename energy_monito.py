
# Smart Energy Monitoring System

# Get electrical readings
voltage = float(input("Enter voltage (V): "))
current = float(input("Enter current (A): "))
power_factor = float(input("Enter power factor: "))
hours = float(input("Enter usage time (hours): "))
tariff = float(input("Enter electricity tariff per unit (Rs): "))

# Input validation
if voltage <= 0:
    print("Invalid voltage!")

elif current < 0:
    print("Invalid current!")

elif power_factor < 0 or power_factor > 1:
    print("Invalid power factor!")

elif hours <= 0:
    print("Invalid usage time!")

elif tariff < 0:
    print("Invalid tariff!")

else:
    # Calculate active power
    power = voltage * current * power_factor

    # Calculate energy consumption
    energy = (power * hours) / 1000

    # Calculate electricity bill
    bill = energy * tariff

    # Display results
    print("\n----- Smart Energy Monitoring System -----")
    print("Voltage:", voltage, "V")
    print("Current:", current, "A")
    print("Power Factor:", power_factor)
    print("Active Power:", power, "W")
    print("Usage Time:", hours, "hours")
    print("Energy Consumption:", energy, "kWh")
    print("Electricity Bill: Rs.", round(bill, 2))
