 
import streamlit as st
import pandas as pd
import os

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

file_name = "energy_data.csv"

if os.path.exists(file_name):
    df = pd.read_csv(file_name)

    if not df.empty and {"Date", "Appliance", "Energy"}.issubset(df.columns):

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Energy"] = pd.to_numeric(df["Energy"], errors="coerce")
        df = df.dropna(subset=["Date", "Energy"])

        if not df.empty:
            tariff = st.sidebar.number_input(
                "Tariff (Rs/unit)", min_value=0.0, value=8.0
            )
            limit = st.sidebar.number_input(
                "Daily alert limit (kWh)", min_value=0.1, value=5.0
            )

            total_energy = df["Energy"].sum()
            total_bill = total_energy * tariff
            total_appliances = df["Appliance"].nunique()

            c1, c2, c3 = st.columns(3)
            c1.metric("⚡ Total Energy", f"{total_energy:.2f} kWh")
            c2.metric("💰 Estimated Bill", f"₹{total_bill:.2f}")
            c3.metric("🔌 Appliances", total_appliances)

            st.divider()

            df["Day"] = df["Date"].dt.date

            left, right = st.columns(2)

            with left:
                st.subheader("📈 Daily Energy Consumption")
                daily = df.groupby("Day")["Energy"].sum()
                st.line_chart(daily)

            with right:
                st.subheader("🔋 Appliance-wise Usage")
                appliance = df.groupby("Appliance")["Energy"].sum()
                st.bar_chart(appliance)

            st.divider()
            st.subheader("🚨 Energy Usage Alert")

            high_usage = daily[daily > limit]

            if not high_usage.empty:
                st.warning("High energy consumption detected!")
                st.dataframe(high_usage)
            else:
                st.success("Energy consumption is within the set limit.")

            st.subheader("📋 Appliance Records")
            st.dataframe(df, use_container_width=True)

        else:
            st.warning("No valid energy readings found.")

    else:
        st.warning("CSV file is empty or has an unexpected format.")

else:
    st.info("Run data_storage.py to add appliance readings.")
