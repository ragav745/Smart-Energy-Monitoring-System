⚡ Smart Energy Monitoring System
Project Overview
The Smart Energy Monitoring System is a Python-based application designed to calculate, store, and visualize electrical energy consumption of household appliances.
It helps users monitor appliance-wise energy usage and estimate electricity bills.
Technologies Used

Python 3
Streamlit
Pandas
Matplotlib
CSV File Handling

Features

Calculate active power using voltage, current, and power factor.
Calculate energy consumption in kWh.
Estimate electricity bills.
Monitor multiple household appliances.
Store energy readings in a CSV file.
Display an interactive dashboard.
Visualize daily and appliance-wise energy consumption.
Generate high-energy consumption alerts.

Project Structure
Smart_Energy_Monitoring/
│
├── energy_monitor.py
├── appliance_monitor.py
├── data_storage.py
├── dashboard.py
├── energy_data.csv
└── README.md

How to Run
1. Install the required libraries
python -m pip install streamlit pandas matplotlib

2. Run the energy calculator
python energy_monitor.py

3. Run the appliance monitor
python appliance_monitor.py

4. Store appliance readings
python data_storage.py

5. Launch the dashboard
python -m streamlit run dashboard.py

Energy Calculation
Active Power:
P = V × I × PF
Energy Consumption:
Energy (kWh) = Power (W) × Time (hours) / 1000
Estimated Electricity Bill:
Bill = Energy Consumption × Tariff
Important Note
This project currently uses manually entered or simulated electrical readings. It does not yet connect to physical sensors or smart meters.
Developed By
EEE Student
Future Enhancements

Real-time sensor integration
IoT-based energy monitoring
Automatic appliance monitoring
Monthly energy reports
## Dashboard Preview

The dashboard provides:
- Total energy consumption
- Estimated electricity bill
- Appliance-wise consumption chart
- Daily energy monitoring
- High consumption alerts
