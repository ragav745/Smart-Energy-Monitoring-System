
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "energy_data.csv")


def load_data():
    try:
        df = pd.read_csv(FILE_NAME)
        df.columns = df.columns.str.strip()

        required = ["Appliance", "Energy_kWh"]

        for column in required:
            if column not in df.columns:
                print("Missing column:", column)
                return None

        df["Energy_kWh"] = pd.to_numeric(
            df["Energy_kWh"], errors="coerce"
        )

        df["Appliance"] = (
            df["Appliance"].astype("string").str.strip()
        )

        df = df.dropna(
            subset=["Appliance", "Energy_kWh"]
        )

        df = df[df["Energy_kWh"] >= 0]

        # Treat Fan and fan as the same appliance
        df["Appliance"] = df["Appliance"].str.title()

        return df

    except FileNotFoundError:
        print("Error: energy_data.csv not found!")
        return None

    except Exception as error:
        print("Error:", error)
        return None


def generate_recommendations(df):
    if df is None or df.empty:
        print("No energy readings available.")
        return

    appliance_energy = (
        df.groupby("Appliance")["Energy_kWh"]
        .sum()
        .sort_values(ascending=False)
    )

    total_energy = appliance_energy.sum()

    print("\n====================================")
    print(" SMART ENERGY-SAVING RECOMMENDATIONS")
    print("====================================")

    print("Total Energy Consumption:",
          round(total_energy, 2), "kWh")

    print("\nAppliance-wise Consumption:")

    for name, energy in appliance_energy.items():
        percentage = (
            energy / total_energy * 100
            if total_energy > 0 else 0
        )

        print(
            name, ":",
            round(energy, 2), "kWh",
            "(", round(percentage, 1), "% )"
        )

    print("\n----- ENERGY-SAVING SUGGESTIONS -----")

    highest_appliance = appliance_energy.idxmax()
    highest_energy = appliance_energy.max()

    print(
        "\n1. Highest consumption:",
        highest_appliance,
        "-", round(highest_energy, 2), "kWh"
    )

    print(
        "   Suggestion: Monitor its daily usage "
        "and switch it off when not required."
    )

    for name, energy in appliance_energy.items():

        if energy > 3:
            print(
                "\n2. ", name,
                "has high recorded consumption."
            )
            print(
                "   Suggestion: Reduce operating hours "
                "and use an energy-efficient model."
            )

        elif energy > 0:
            print(
                "\n3. ", name,
                "has recorded consumption of",
                round(energy, 2), "kWh."
            )
            print(
                "   Suggestion: Avoid unnecessary "
                "operation to save electricity."
            )

    print("\nRecommendations generated successfully!")


def main():
    df = load_data()

    if df is not None:
        generate_recommendations(df)


if __name__ == "__main__":
    main()
