import sqlite3
import pandas as pd
conn = sqlite3.connect("fitbit_database.db")

def verify_total_steps(conn):
    """
    Verify whether the TotalSteps variable for each individual on a day matches the sum of the StepTotal
    in the hourly_steps table using SQL.
    
    Parameters:
    - conn: SQLite database connection
    
    Returns:
    - True if all values match, False if mismatches are found.
    """

    query = """
    SELECT d.Id, d.ActivityDate, d.TotalSteps AS DailyTotalSteps, SUM(h.StepTotal) AS SumHourlySteps
    FROM daily_activity d
    JOIN hourly_steps h 
        ON d.Id = h.Id 
        AND date(d.ActivityDate) = date(h.ActivityHour)
    GROUP BY d.Id, d.ActivityDate
    HAVING DailyTotalSteps != SumHourlySteps;
    """

    mismatches = pd.read_sql(query, conn)

    if mismatches.empty:
        print("No mismatches in TotalSteps in daily_activity and sum of hourly_steps.")
    else:
        print("There are mismatches in TotalSteps in daily_activity and sum of hourly_steps:")
        print(mismatches)
