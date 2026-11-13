
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "energy_data.csv")

st.set_page_config(
    page_title="Smart Energy Monitoring",
    page_icon="⚡",
    layout="wide"
)

# Dashboard styling
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

# Load CSV
@st.cache_data
def load_data():
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame()

    df = pd.read_csv(FILE_NAME)
    df.columns = df.columns.str.strip()

    required = [
        "Date", "Appliance", "Energy_kWh", "Bill_Rs"
    ]

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

    # Combine Fan and fan
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

    df = df[df["Energy_kWh"] >= 0]

    return df


df = load_data()

if df.empty:
    st.warning("No complete energy readings found.")
    st.info("Add readings using energy_monitor.py.")
    st.stop()

# Sidebar filters
st.sidebar.subheader("Filters")

appliances = sorted(df["Appliance"].unique())

selected_appliances = st.sidebar.multiselect(
    "Select Appliances",
    appliances,
    default=appliances
)

filtered_df = df[
    df["Appliance"].isin(selected_appliances)
]

if filtered_df.empty:
    st.info("Select at least one appliance.")
    st.stop()

# Summary metrics
total_energy = filtered_df["Energy_kWh"].sum()
total_bill = filtered_df["Bill_Rs"].sum()
total_appliances = filtered_df["Appliance"].nunique()
total_readings = len(filtered_df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("⚡ Total Energy", f"{total_energy:.2f} kWh")
c2.metric("💰 Electricity Bill", f"₹{total_bill:.2f}")
c3.metric("🔌 Appliances", total_appliances)
c4.metric("📋 Readings", total_readings)

st.divider()

# Consumption charts
st.subheader("📈 Energy Consumption Analysis")

filtered_df = filtered_df.copy()
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

# Appliance recommendations
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

# Records
st.subheader("📋 Appliance Records")

st.dataframe(
    filtered_df.sort_values("Date", ascending=False),
    use_container_width=True
)

# Download CSV
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Energy Records",
    data=csv_data,
    file_name="energy_records.csv",
    mime="text/csv"
)

st.success("Smart Energy Monitoring Dashboard loaded successfully!")
