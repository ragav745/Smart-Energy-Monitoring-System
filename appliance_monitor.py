
# Multiple Appliance Energy Monitoring

appliances = []

n = int(input("Enter number of appliances: "))

for i in range(n):
    print("\nAppliance", i + 1)

    name = input("Enter appliance name: ")
    power = float(input("Enter power in watts: "))
    hours = float(input("Enter daily usage hours: "))

    energy = (power * hours) / 1000

    appliance = {
        "name": name,
        "power": power,
        "hours": hours,
        "energy": energy
    }

    appliances.append(appliance)

print("\n----- Appliance Energy Report -----")

total_energy = 0

for appliance in appliances:
    print(appliance["name"], "-", appliance["energy"], "kWh")
    total_energy += appliance["energy"]

print("Total Daily Energy:", total_energy, "kWh")
