import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Read Weather Data from CSV
def get_csv_weather_data(csv_path="Chicago 2016-03-25 to 2016-04-12.csv"):
    """
    Reads weather data from a local CSV file and processes it.
    """
    df_csv = pd.read_csv(csv_path)

    # Print column names to verify
    print("Weather CSV Columns:", df_csv.columns)
    
    # Rename and process date column
    if 'datetime' in df_csv.columns:
        df_csv.rename(columns={'datetime': 'date'}, inplace=True)
    elif 'Date' in df_csv.columns:
        df_csv.rename(columns={'Date': 'date'}, inplace=True)

    df_csv['date'] = pd.to_datetime(df_csv['date'])

    return df_csv

# Load weather data
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

weather_factors = ["temp", "humidity", "precip", "windspeed"]
avg_steps_weather = df_merged[weather_factors + ["TotalSteps"]].corr()["TotalSteps"].drop("TotalSteps")

df_avg_steps_weather = pd.DataFrame(avg_steps_weather).reset_index()
df_avg_steps_weather.columns = ["Weather Factor", "Correlation with Steps"]

plt.figure(figsize=(8, 6))
sns.barplot(x=df_avg_steps_weather["Weather Factor"], y=df_avg_steps_weather["Correlation with Steps"], palette="Blues_r")
plt.xlabel("Weather Factors")
plt.ylabel("Correlation with Steps")
plt.title("Correlation of Weather Factors with Total Steps")
plt.xticks(rotation=45)
plt.show()