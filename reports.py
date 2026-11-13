
import pandas as pd
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "energy_data.csv")


def load_data():
    try:
        df = pd.read_csv(FILE_NAME)
        df.columns = df.columns.str.strip()

        required = ["Date", "Appliance", "Energy_kWh", "Bill_Rs"]

        for column in required:
            if column not in df.columns:
                print("Missing column:", column)
                return None

        df["Date"] = pd.to_datetime(
            df["Date"], format="mixed", errors="coerce"
        )

        df["Energy_kWh"] = pd.to_numeric(
            df["Energy_kWh"], errors="coerce"
        )

        df["Bill_Rs"] = pd.to_numeric(
            df["Bill_Rs"], errors="coerce"
        )

        df["Appliance"] = df["Appliance"].astype("string").str.strip()

        df = df.dropna(
            subset=["Date", "Appliance", "Energy_kWh", "Bill_Rs"]
        )

        return df

    except FileNotFoundError:
        print("Error: energy_data.csv not found!")
        return None
    except pd.errors.EmptyDataError:
        print("CSV file is empty!")
        return None
    except Exception as error:
        print("Error loading data:", error)
        return None


def show_report(data, title):
    print("\n================================")
    print(title)
    print("================================")

    if data.empty:
        print("No readings available for this period.")
        return

    print("Total Readings:", len(data))
    print("Total Energy:", round(data["Energy_kWh"].sum(), 2), "kWh")
    print("Total Bill: Rs.", round(data["Bill_Rs"].sum(), 2))

    print("\nAppliance-wise Energy:")
    print(
        data.groupby("Appliance")["Energy_kWh"]
        .sum()
        .round(2)
        .to_string()
    )


def daily_report(df):
    today = datetime.now().date()
    data = df[df["Date"].dt.date == today]
    show_report(data, "DAILY ENERGY REPORT")


def weekly_report(df):
    today = datetime.now().date()
    start = today - timedelta(days=6)

    data = df[
        (df["Date"].dt.date >= start) &
        (df["Date"].dt.date <= today)
    ]

    show_report(data, "LAST 7 DAYS REPORT")


def monthly_report(df):
    now = datetime.now()

    data = df[
        (df["Date"].dt.month == now.month) &
        (df["Date"].dt.year == now.year)
    ]

    show_report(data, "MONTHLY ENERGY REPORT")


def date_range_report(df):
    try:
        print("\nEnter dates in YYYY-MM-DD format")

        start = datetime.strptime(
            input("Start date: ").strip(), "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            input("End date: ").strip(), "%Y-%m-%d"
        ).date()

        if start > end:
            print("Start date cannot be after end date!")
            return None

        data = df[
            (df["Date"].dt.date >= start) &
            (df["Date"].dt.date <= end)
        ]

        show_report(data, "CUSTOM DATE-RANGE REPORT")

        return data

    except ValueError:
        print("Invalid date! Use YYYY-MM-DD.")
        return None


def export_report(data):
    if data is None or data.empty:
        print("No readings available to export.")
        return

    filename = os.path.join(BASE_DIR, "energy_report.csv")

    try:
        data.to_csv(filename, index=False)
        print("\nReport exported successfully!")
        print("File:", filename)

    except PermissionError:
        print("Close energy_report.csv if it is open and try again.")

    except Exception as error:
        print("Export error:", error)


def main():
    df = load_data()

    if df is None:
        return

    if df.empty:
        print("No complete energy readings found.")
        return

    print("\nComplete readings loaded:", len(df))

    while True:
        print("\n===== SMART ENERGY REPORT SYSTEM =====")
        print("1. Daily Report")
        print("2. Weekly Report")
        print("3. Monthly Report")
        print("4. Custom Date-Range Report")
        print("5. Export All Readings to CSV")
        print("6. Export Custom Date-Range to CSV")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            daily_report(df)

        elif choice == "2":
            weekly_report(df)

        elif choice == "3":
            monthly_report(df)

        elif choice == "4":
            date_range_report(df)

        elif choice == "5":
            export_report(df)

        elif choice == "6":
            selected_data = date_range_report(df)
            if selected_data is not None:
                export_report(selected_data)

        elif choice == "7":
            print("Report system closed.")
            break

        else:
            print("Invalid choice! Select 1 to 7.")


if __name__ == "__main__":
    main()
