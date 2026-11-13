from data_storage import save_reading


def validate_inputs(voltage, current, power_factor, hours, tariff):
    if voltage <= 0:
        return False
    elif current < 0:
        return False
    elif power_factor < 0 or power_factor > 1:
        return False
    elif hours <= 0:
        return False
    elif tariff < 0:
        return False
    return True


def calculate_power(voltage, current, power_factor):
    return voltage * current * power_factor


def calculate_energy(power, hours):
    return (power * hours) / 1000


def calculate_bill(energy, tariff):
    return energy * tariff


def main():
    try:
        print("\n===== SMART ENERGY MONITORING SYSTEM =====")

        appliance = input("Enter appliance name: ")
        voltage = float(input("Enter voltage (V): "))
        current = float(input("Enter current (A): "))
        power_factor = float(input("Enter power factor (0 to 1): "))
        hours = float(input("Enter usage time (hours): "))
        tariff = float(input("Enter electricity tariff per unit (Rs): "))

        if validate_inputs(voltage, current, power_factor, hours, tariff):

            power = calculate_power(voltage, current, power_factor)
            energy = calculate_energy(power, hours)
            bill = calculate_bill(energy, tariff)

            #save_reading(appliance, voltage, current, power, hours, energy, tariff, bill   )
            save_reading(
    appliance, voltage, current, power,
    hours, energy, tariff, bill
)

            print("\n----- ENERGY CONSUMPTION REPORT -----")
            print("Appliance:", appliance)
            print("Voltage:", voltage, "V")
            print("Current:", current, "A")
            print("Power Factor:", power_factor)
            print("Active Power:", round(power, 2), "W")
            print("Usage Time:", hours, "hours")
            print("Energy Consumption:", round(energy, 2), "kWh")
            print("Electricity Bill: Rs.", round(bill, 2))

        else:
            print("Invalid input! Please check your values.")

    except ValueError:
        print("Error: Please enter numbers only!")

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")


if __name__ == "__main__":
    main()
