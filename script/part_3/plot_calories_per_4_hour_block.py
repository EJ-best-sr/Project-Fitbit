import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

connection = sqlite3.connect("data/fitbit_database.db")

def plot_calories_per_4_hour_block():
    """
    Plots the average calories burnt per 4-hour time block.

    Data is retrieved from an SQLite database table named 'hourly_calories'.
    The function processes the calorie data, categorizes it into 4-hour blocks,
    calculates the average calories burnt for each block, and visualizes it
    using a bar chart.

    Parameters:
        None

    Returns:
        None (Displays a matplotlib bar chart)
    """
    query = "SELECT ActivityHour, Calories FROM hourly_calories"
    hourly_calories = pd.read_sql_query(query, connection)
    
    hourly_calories["ActivityHour"] = pd.to_datetime(hourly_calories["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    hourly_calories["HourBlock"] = hourly_calories["ActivityHour"].dt.hour // 4 * 4
    
    calories_avg = hourly_calories.groupby("HourBlock")["Calories"].mean()
    
    hour_labels = {i: f"{i}-{i+4}" for i in range(0, 24, 4)}
    calories_avg.index = calories_avg.index.map(hour_labels)
    
    cmap = sns.color_palette("viridis", as_cmap=True)
    norm = plt.Normalize(vmin=min(calories_avg.values), vmax=max(calories_avg.values))
    colors = [cmap(norm(value)) for value in calories_avg.values]
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(calories_avg.index, calories_avg.values, color=colors)
    ax.set_title("Average Calories Burnt per 4-Hour Block")
    ax.set_xlabel("Time Block")
    ax.set_ylabel("Average Calories")
    
    plt.show()
