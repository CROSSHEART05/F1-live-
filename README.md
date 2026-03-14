# 🏎 Formula 1 Live Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Data Source](https://img.shields.io/badge/Data-OpenF1%20%7C%20FastF1-orange)

A **real-time Formula 1 analytics dashboard** built using **Python and Streamlit** that visualizes live race data, lap statistics, and official session results.
The dashboard integrates **OpenF1 telemetry data** and **FastF1 timing data** to provide insights similar to professional motorsport analytics platforms.

---

# 📸 Dashboard Preview

![Dashboard Screenshot](images/dashboard_preview.png)

*(Add a screenshot of your Streamlit dashboard here after running it.)*

---

# 🚀 Features

### 🏁 Grand Prix Selection

Select any race from the current Formula 1 season calendar.

### 📊 Session Selection

View data from multiple session types:

* Practice 1 / Practice 2 / Practice 3
* Sprint Shootout
* Sprint
* Qualifying
* Race

### 🏎 Live Race Positions

Displays real-time driver positions during the session.

### ⏱ Lap Leaderboard

Shows driver lap times sorted by fastest laps.

### ⚡ Fastest Lap Detection

Automatically identifies the fastest lap recorded.

### 🏆 Final Session Results

Displays official session results using FastF1 timing data.

### 🔄 Auto Refresh

The dashboard refreshes automatically to display updated race data.

---

# 🛠 Technologies Used

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| **Python**     | Core programming language       |
| **Streamlit**  | Interactive dashboard framework |
| **Pandas**     | Data manipulation and analysis  |
| **Requests**   | Fetching data from APIs         |
| **FastF1**     | Official F1 timing data         |
| **OpenF1 API** | Live telemetry and race data    |

---

# 📊 Data Sources

### OpenF1 API

Provides live telemetry, lap data, positions, and driver information.

https://openf1.org/

### FastF1 Python Library

Provides official Formula 1 timing data, event schedules, and session results.

https://theoehrly.github.io/Fast-F1/

---

# ⚙ Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/CROSSHEART05/f1-live.git
cd f1-live
```

---

## 2️⃣ Install dependencies

```bash
pip install streamlit pandas requests fastf1 streamlit-autorefresh
```

---

## 3️⃣ Run the dashboard

```bash
python -m streamlit run f1_dashboard.py
```

The dashboard will open in your browser:

```
http://localhost:8501
```

---


# 🧠 How the Dashboard Works

### 1️⃣ Event Schedule

FastF1 retrieves the official Formula 1 race calendar.

### 2️⃣ Session Selection

Users select a Grand Prix and session.

### 3️⃣ Session Key Retrieval

The OpenF1 API returns the session key used to access session telemetry data.

### 4️⃣ Data Processing

The API responses are converted into Pandas DataFrames.

### 5️⃣ Visualization

Streamlit renders the processed data as tables, metrics, and analytics panels.

---

# 🔄 Auto Refresh

The dashboard refreshes automatically to update live race data.

```python
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=15000, key="f1_refresh")
```

Refresh interval: **15 seconds**

---

# 📈 Future Improvements

Planned enhancements include:

* 📉 **Lap Time Evolution Graphs**
* 🟡 **Pit Stop Analysis**
* 🟣 **Tyre Strategy Visualization**
* 🏎 **Driver Telemetry Comparison**
* 📊 **Sector Time Analysis**
* 🔁 **Overtake Detection**

---

# 🎯 Purpose of the Project

This project demonstrates:

* API-based data pipelines
* real-time sports analytics
* dashboard development
* data visualization with Python

It is designed as a **portfolio project for Data Science, AI, and Machine Learning roles**.

---

# 👨‍💻 Author

**Akshat Kumar Chauhan**

Computer Science Engineering Student
AI / Machine Learning Enthusiast

---

# 📜 License

This project is licensed under the **MIT License**.

---

⭐ If you found this project useful, consider **starring the repository**!
