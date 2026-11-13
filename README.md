
# ⚡ Smart Energy Monitoring System

A Python-based Smart Energy Monitoring System developed as an Electrical and Electronics Engineering project.

## 📌 Project Overview

This project calculates and monitors electrical energy consumption and estimated electricity costs for different household appliances.

It stores readings in CSV files and displays consumption data through an interactive Streamlit dashboard.

**Note:** The current version uses manually entered or simulated readings, not live hardware sensors.

## 🎯 Objectives

- Calculate electrical power using voltage, current and power factor.
- Calculate energy consumption in kWh.
- Estimate electricity bills.
- Monitor multiple appliances.
- Generate daily, weekly and monthly reports.
- Provide energy-saving recommendations.
- Visualize consumption through a dashboard.

## 🚀 Features

- Voltage, current and power factor input
- Active power calculation
- Energy consumption calculation
- Electricity bill calculation
- Appliance management using OOP
- CSV data storage
- Appliance add, update and delete operations
- Daily, weekly and monthly reports
- Energy-saving recommendations
- Interactive Streamlit dashboard
- CSV report download

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- CSV

## 📂 Project Structure

```text
Smart_Energy_Monitoring/
│
├── energy_monitor.py
├── appliance_monitor.py
├── data_storage.py
├── dashboard.py
├── reports.py
├── recommendations.py
├── energy_data.csv
├── appliances.csv
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Install the required packages:

```bash
python -m pip install streamlit pandas matplotlib
```

## ▶️ How to Run

Run the energy monitoring program:

```bash
python energy_monitor.py
```

Run appliance management:

```bash
python appliance_monitor.py
```

Generate reports:

```bash
python reports.py
```

Generate recommendations:

```bash
python recommendations.py
```

Launch the dashboard:

```bash
streamlit run dashboard.py
```

## 📊 Dashboard

The dashboard provides:

- Total energy consumption
- Estimated electricity bill
- Appliance-wise consumption chart
- Daily energy consumption chart
- High-consumption alerts
- Energy-saving recommendations
- Appliance reading records
- CSV download

## 🔮 Future Enhancements

- Real-time sensor integration
- IoT-based energy monitoring
- Live electricity consumption tracking
- Mobile application integration
- Advanced prediction and analytics

## 👨‍💻 Project Domain

Electrical and Electronics Engineering (EEE)

## 📄 License

This project is developed for academic and educational purposes.
