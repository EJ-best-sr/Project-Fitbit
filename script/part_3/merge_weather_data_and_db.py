import sqlite3
import pandas as pd
from read_weather_data import get_weather_data, get_csv_weather_data
conn = sqlite3.connect("fitbit_database.db")

# load the daily_activity table into a DataFrame
daily_df = pd.read_sql_query("""
    SELECT Id, ActivityDate, TotalSteps, TotalDistance, 
           VeryActiveMinutes, LightlyActiveMinutes, SedentaryMinutes, Calories
    FROM daily_activity
""", conn)

conn.close()

daily_df['ActivityDate'] = pd.to_datetime(daily_df['ActivityDate'])

daily_df.head()
weather_data_api = get_weather_data()

weather_data_api['datetime'] = pd.to_datetime(weather_data_api['datetime'], errors='coerce')
weather_data_api.head()

# clear missing values columns before merging
columns_to_drop = ['solarradiation', 'solarenergy', 'uvindex', 'severerisk']
weather_data_api.drop(columns = columns_to_drop, axis = 1, inplace = True)

# merging
merged_df = pd.merge(daily_df, weather_data_api, left_on = 'ActivityDate', right_on = 'datetime', how = 'inner')
merged_df