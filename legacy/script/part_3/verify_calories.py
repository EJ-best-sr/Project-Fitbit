import sqlite3
import pandas as pd

conn = sqlite3.connect("fitbit_database.db")

def verify_calories_match_hourly(conn):
    """
    Verify whether the Calories variable for each individual on a day matches the sum of the calories
    in the hourly_calories table using SQL.
    
    Parameters:
    - conn: SQLite database connection
    """

    query = """
    SELECT d.Id, d.ActivityDate, d.Calories AS DailyCalories, SUM(h.Calories) AS SumHourlyCalories
    FROM daily_activity d
    JOIN hourly_calories h 
        ON d.Id = h.Id 
        AND date(d.ActivityDate) = date(h.ActivityHour)
    GROUP BY d.Id, d.ActivityDate
    HAVING DailyCalories != SumHourlyCalories;
    """

    mismatches = pd.read_sql(query, conn)

    if mismatches.empty:
        print("No mismatches in Calories in daily_activity and in hourly_calories.")
    else:
        print("There are mismatches in Calories in daily_activity and in hourly_calories:")
        print(mismatches)

