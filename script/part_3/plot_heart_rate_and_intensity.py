import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

conn = sqlite3.connect("/Users/elvirabest/Downloads/fitbit_database.db")

def plot_heart_rate_and_intensity(user_id):
    user_id = int(user_id)
    query_intensity = "SELECT Id, TotalIntensity FROM hourly_intensity WHERE Id = ?"
    query_heart_rate = "SELECT Id, Time, Value FROM heart_rate WHERE Id = ?"
    hourly_intensity = pd.read_sql_query(query_intensity, conn, params=(user_id,))
    heart_rate = pd.read_sql_query(query_heart_rate, conn, params=(user_id,))
    heart_rate["Time"] = pd.to_datetime(heart_rate["Time"], errors="coerce")

    if heart_rate.empty:
        print(f"No heart rate data found for user ID: {user_id}")
        return

    total_intensity = hourly_intensity["TotalIntensity"].sum() if not hourly_intensity.empty else 0
    heart_rate["Time_Blocked"] = heart_rate["Time"].dt.floor("4H")
    four_hourly_avg = heart_rate.groupby("Time_Blocked")["Value"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    scatter = ax.scatter(heart_rate["Time"], heart_rate["Value"], c=heart_rate["Time"].astype(int), cmap="viridis", alpha=0.6, label="Raw Heart Rate Data")
    ax.plot(four_hourly_avg["Time_Blocked"], four_hourly_avg["Value"], color="black", marker="o", linestyle="-", linewidth=2, label="4-Hour Avg Heart Rate")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45, fontsize=10)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Heart Rate (BPM)", fontsize=12)
    ax.set_title("4-Hour Average Heart Rate", fontsize=14, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.text(0.5, 0.9, f"Total Intensity: {total_intensity}", transform=ax.transAxes,
             fontsize=14, ha="center", bbox=dict(facecolor="white", edgecolor="black"))
    ax.legend()
    plt.tight_layout()
    plt.show()

plot_heart_rate_and_intensity(2022484408.0)