import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

connection = sqlite3.connect("fitbit_database.db")

def plot_sleep_per_4_hour_block():
    query = "SELECT date, value FROM minute_sleep"
    minute_sleep = pd.read_sql_query(query, connection)
    minute_sleep["date"] = pd.to_datetime(minute_sleep["date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    minute_sleep["HourBlock"] = minute_sleep["date"].dt.hour // 4 * 4
    sleep_avg = minute_sleep.groupby("HourBlock")["value"].mean()
    hour_labels = {i: f"{i}-{i+4}" for i in range(0, 24, 4)}
    sleep_avg.index = sleep_avg.index.map(hour_labels)
    cmap = sns.color_palette("viridis", as_cmap=True)
    norm = plt.Normalize(vmin=min(sleep_avg.values), vmax=max(sleep_avg.values))
    colors = [cmap(norm(value)) for value in sleep_avg.values]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(sleep_avg.index, sleep_avg.values, color=colors)
    ax.set_title("Average Minutes of Sleep per 4-Hour Block")
    ax.set_xlabel("Time Block")
    ax.set_ylabel("Average Minutes Asleep")
    plt.show()