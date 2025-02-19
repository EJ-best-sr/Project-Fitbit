import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

sns.set_palette("viridis")

# Connect to the database
connection = sqlite3.connect("/Users/elvirabest/Downloads/fitbit_database.db")

# Function to create readable 4-hour block labels
def get_hour_block_labels():
    return {i: f"{i}-{i+4}" for i in range(0, 24, 4)}

hour_labels = get_hour_block_labels()

# Function: Visualize 4-hour activity blocks for steps
def visualize_steps_per_4_hour_block():
    query = "SELECT ActivityHour, StepTotal FROM hourly_steps"
    hourly_steps = pd.read_sql_query(query, connection)
    hourly_steps['ActivityHour'] = pd.to_datetime(hourly_steps['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    hourly_steps['HourBlock'] = hourly_steps['ActivityHour'].dt.hour // 4 * 4
    step_avg = hourly_steps.groupby('HourBlock')['StepTotal'].mean()
    
    plt.figure(figsize=(10, 5))
    plt.bar([hour_labels[h] for h in step_avg.index], step_avg.values)
    plt.title('Average Steps per 4-Hour Block')
    plt.xlabel('Time Block')
    plt.ylabel('Average Steps')
    plt.show()

# Function: Visualize 4-hour activity blocks for calories burnt
def visualize_calories_per_4_hour_block():
    query = "SELECT ActivityHour, Calories FROM hourly_calories"
    hourly_calories = pd.read_sql_query(query, connection)
    hourly_calories['ActivityHour'] = pd.to_datetime(hourly_calories['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    hourly_calories['HourBlock'] = hourly_calories['ActivityHour'].dt.hour // 4 * 4
    calories_avg = hourly_calories.groupby('HourBlock')['Calories'].mean()
    
    plt.figure(figsize=(10, 5))
    plt.bar([hour_labels[h] for h in calories_avg.index], calories_avg.values)
    plt.title('Average Calories Burnt per 4-Hour Block')
    plt.xlabel('Time Block')
    plt.ylabel('Average Calories')
    plt.show()

# Function: Visualize 4-hour activity blocks for minutes of sleep (now using "Value")
def visualize_sleep_per_4_hour_block():
    query = "SELECT date, value FROM minute_sleep"
    minute_sleep = pd.read_sql_query(query, connection)
    minute_sleep['date'] = pd.to_datetime(minute_sleep['date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    minute_sleep['HourBlock'] = minute_sleep['date'].dt.hour // 4 * 4
    sleep_avg = minute_sleep.groupby('HourBlock')['value'].mean()
    
    plt.figure(figsize=(10, 5))
    plt.bar([hour_labels[h] for h in sleep_avg.index], sleep_avg.values)
    plt.title('Average Minutes of Sleep per 4-Hour Block')
    plt.xlabel('Time Block')
    plt.ylabel('Average Minutes Asleep')
    plt.show()


visualize_sleep_per_4_hour_block()









