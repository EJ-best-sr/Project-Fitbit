import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_csv_weather_data(csv_path="Chicago 2016-03-25 to 2016-04-12.csv"):
    """
    Reads weather data from a local CSV file and processes it.
    """
    df_csv = pd.read_csv(csv_path)

   
    
    if 'datetime' in df_csv.columns:
        df_csv.rename(columns={'datetime': 'date'}, inplace=True)
    elif 'Date' in df_csv.columns:
        df_csv.rename(columns={'Date': 'date'}, inplace=True)

    df_csv['date'] = pd.to_datetime(df_csv['date'])

    return df_csv

weather_csv_path = "Chicago 2016-03-25 to 2016-04-12.csv"
df_weather = get_csv_weather_data(weather_csv_path)

# Step 2: Extract Fitbit Data from SQLite Database
db_path = "fitbit_database.db"

# Connect to the database
conn = sqlite3.connect(db_path)

# Load daily activity table
query = """
SELECT Id, ActivityDate, TotalSteps, VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes 
FROM daily_activity
"""
df_fitbit = pd.read_sql(query, conn)

df_fitbit.rename(columns={'ActivityDate': 'date'}, inplace=True)
df_fitbit['date'] = pd.to_datetime(df_fitbit['date'])

conn.close()

df_merged = pd.merge(df_fitbit, df_weather, on="date", how="inner")

print(df_merged.head())  # Display first few rows

df_merged["Rainy"] = df_merged["precip"] > 0  # Define rainy days

plt.figure(figsize=(8, 6))
sns.boxplot(x=df_merged["Rainy"], y=df_merged["TotalSteps"])
plt.xlabel("Rainy Day (True/False)")
plt.ylabel("Total Steps")
plt.title("Total Steps on Rainy vs Non-Rainy Days")
plt.show()