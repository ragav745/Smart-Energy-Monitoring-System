
import os
import calendar
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "energy_data.csv")

st.set_page_config(
    page_title="Smart Energy Monitoring",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: white;
}
[data-testid="stMetric"] {
    background: #17243a;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263c59;
}
h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Smart Energy Monitoring System")
st.caption("Electrical Energy Analysis | EEE Project")

st.sidebar.title("⚡ Energy Monitor")
st.sidebar.write("Dashboard Navigation")
st.sidebar.info("Monitor electricity usage and estimated cost.")


# Load data
@st.cache_data
def load_data():

    if not os.path.exists(FILE_NAME):
        return pd.DataFrame()

    df = pd.read_csv(FILE_NAME)
    df.columns = df.columns.str.strip()

    required = ["Date", "Appliance", "Energy_kWh", "Bill_Rs"]

    if not all(column in df.columns for column in required):
        return pd.DataFrame()

    df["Date"] = pd.to_datetime(
        df["Date"], format="mixed", errors="coerce"
    )

    df["Energy_kWh"] = pd.to_numeric(
        df["Energy_kWh"], errors="coerce"
    )

    df["Bill_Rs"] = pd.to_numeric(
        df["Bill_Rs"], errors="coerce"
    )

    df["Appliance"] = (
        df["Appliance"]
        .astype("string")
        .str.strip()
        .str.casefold()
        .str.title()
    )

    df = df.dropna(
        subset=["Date", "Appliance", "Energy_kWh", "Bill_Rs"]
    )

    df = df[
        (df["Energy_kWh"] >= 0) &
        (df["Bill_Rs"] >= 0)
    ]

    return df


df = load_data()

if df.empty:
    st.warning("No complete energy readings found.")
    st.info("Add readings using energy_monitor.py.")
    st.stop()


# Appliance filter
st.sidebar.subheader("Filters")

appliances = sorted(df["Appliance"].unique())

selected_appliances = st.sidebar.multiselect(
    "Select Appliances",
    appliances,
    default=appliances
)

filtered_df = df[
    df["Appliance"].isin(selected_appliances)
].copy()

if filtered_df.empty:
    st.info("Select at least one appliance.")
    st.stop()


# Summary metrics
total_energy = filtered_df["Energy_kWh"].sum()
total_bill = filtered_df["Bill_Rs"].sum()
total_appliances = filtered_df["Appliance"].nunique()
total_readings = len(filtered_df)


# Monthly prediction
today = datetime.now()

current_month_data = filtered_df[
    (filtered_df["Date"].dt.month == today.month) &
    (filtered_df["Date"].dt.year == today.year)
]

monthly_energy = current_month_data["Energy_kWh"].sum()
monthly_bill = current_month_data["Bill_Rs"].sum()

days_in_month = calendar.monthrange(
    today.year, today.month
)[1]

predicted_bill = (
    monthly_bill / today.day
) * days_in_month

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("⚡ Total Energy", f"{total_energy:.2f} kWh")
c2.metric("💰 Electricity Bill", f"₹{total_bill:.2f}")
c3.metric("🔌 Appliances", total_appliances)
c4.metric("📋 Readings", total_readings)
c5.metric("📅 Predicted Monthly Bill", f"₹{predicted_bill:.2f}")

st.caption(
    f"Month-to-date bill for {today.strftime('%B %Y')}: "
    f"₹{monthly_bill:.2f}"
)

st.divider()


# Monthly bill prediction
st.subheader("📅 Monthly Electricity Bill Prediction")

col1, col2 = st.columns(2)

col1.metric(
    "Monthly Energy Consumption",
    f"{monthly_energy:.2f} kWh"
)

col2.metric(
    "Estimated Month-End Bill",
    f"₹{predicted_bill:.2f}"
)

st.info(
    "Prediction uses the average recorded bill per calendar day. "
    "It assumes the average rate continues through the month."
)

st.divider()


# Monthly energy history
st.subheader("📊 Monthly Energy History")

history_df = filtered_df.copy()

history_df["Month"] = (
    history_df["Date"].dt.to_period("M").astype(str)
)

monthly_history = (
    history_df.groupby("Month")
    .agg({
        "Energy_kWh": "sum",
        "Bill_Rs": "sum"
    })
    .sort_index()
)

if not monthly_history.empty:

    left, right = st.columns(2)

    with left:
        st.write("**Monthly Energy Consumption (kWh)**")
        st.bar_chart(monthly_history["Energy_kWh"])

    with right:
        st.write("**Monthly Electricity Bill (₹)**")
        st.bar_chart(monthly_history["Bill_Rs"])

    highest_month = monthly_history["Energy_kWh"].idxmax()
    highest_energy = monthly_history.loc[
        highest_month, "Energy_kWh"
    ]

    st.info(
        f"Highest recorded consumption month: "
        f"{highest_month} ({highest_energy:.2f} kWh)"
    )

    st.write("**Monthly Summary**")
    st.dataframe(
        monthly_history.rename(columns={
            "Energy_kWh": "Energy (kWh)",
            "Bill_Rs": "Bill (₹)"
        }),
        use_container_width=True
    )

else:
    st.info("Monthly history is not available yet.")

st.caption(
    "Monthly history uses the readings currently stored in energy_data.csv. "
    "A month with no readings will not appear."
)

st.divider()


# Daily energy charts
st.subheader("📈 Energy Consumption Analysis")

filtered_df["Day"] = filtered_df["Date"].dt.date

daily = filtered_df.groupby("Day")["Energy_kWh"].sum()

appliance_energy = (
    filtered_df.groupby("Appliance")["Energy_kWh"]
    .sum()
    .sort_values(ascending=False)
)

left, right = st.columns(2)

with left:
    st.write("**Daily Energy Consumption**")
    st.line_chart(daily)

with right:
    st.write("**Appliance-wise Usage**")
    st.bar_chart(appliance_energy)

st.divider()


# Daily alert
st.subheader("🚨 Daily Energy Usage Alert")

limit = st.sidebar.number_input(
    "Daily alert limit (kWh)",
    min_value=0.1,
    value=5.0,
    step=0.5
)

high_usage = daily[daily > limit]

if not high_usage.empty:
    st.warning("High daily energy consumption detected!")
    st.dataframe(high_usage)
else:
    st.success("Daily consumption is within the selected limit.")

st.divider()


# Energy-saving recommendations
st.subheader("💡 Energy-Saving Recommendations")

if not appliance_energy.empty:

    highest_name = appliance_energy.index[0]
    highest_value = appliance_energy.iloc[0]

    st.info(
        f"Highest-consuming appliance: {highest_name} "
        f"({highest_value:.2f} kWh)"
    )

    for name, energy in appliance_energy.items():

        if energy > 3:
            st.warning(
                f"{name}: High recorded consumption. "
                "Reduce unnecessary operating hours."
            )
        else:
            st.write(
                f"• {name}: Switch off when not required."
            )

st.caption(
    "Recommendations are rule-based and use recorded readings. "
    "This project does not currently use live sensors."
)

st.divider()


# Appliance records
st.subheader("📋 Appliance Records")

st.dataframe(
    filtered_df.sort_values("Date", ascending=False),
    use_container_width=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Energy Records",
    data=csv_data,
    file_name="energy_records.csv",
    mime="text/csv"
)

st.success("Smart Energy Monitoring Dashboard loaded successfully!")
