import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

connection = sqlite3.connect("fitbit_database.db")

def plot_steps_per_4_hour_block():
    query = "SELECT ActivityHour, StepTotal FROM hourly_steps"
    hourly_steps = pd.read_sql_query(query, connection)
    hourly_steps["ActivityHour"] = pd.to_datetime(hourly_steps["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    hourly_steps["HourBlock"] = hourly_steps["ActivityHour"].dt.hour // 4 * 4
    step_avg = hourly_steps.groupby("HourBlock")["StepTotal"].mean()
    hour_labels = {i: f"{i}-{i+4}" for i in range(0, 24, 4)}
    step_avg.index = step_avg.index.map(hour_labels)
    cmap = sns.color_palette("viridis", as_cmap=True)
    norm = plt.Normalize(vmin=min(step_avg.values), vmax=max(step_avg.values))
    colors = [cmap(norm(value)) for value in step_avg.values]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(step_avg.index, step_avg.values, color=colors)
    ax.set_title("Average Steps per 4-Hour Block")
    ax.set_xlabel("Time Block")
    ax.set_ylabel("Average Steps")
    plt.show()


