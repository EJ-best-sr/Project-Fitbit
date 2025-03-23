import sqlite3
import pandas as pd

pd.set_option('display.float_format', '{:.0f}'.format)
conn = sqlite3.connect("fitbit_database.db")

def compute_sleep_durations_per_session(conn, user_id):
    """
    Computes sleep duration per session for a specific user.

    Parameters:
    - conn: SQLite database connection
    - user_id: The ID of the user to analyze

    Returns:
    - A DataFrame containing sleep duration per session (logId, SleepDurationMinutes).
    """
    query = """
    SELECT logId, COUNT(logId) AS SleepDurationMinutes
    FROM minute_sleep
    WHERE Id = ?
    GROUP BY logId;
    """
    
    sleep_sessions = pd.read_sql(query, conn, params=(user_id,))
    return sleep_sessions

# user_id = 1503960366 
# print(compute_sleep_durations_per_session(conn, user_id))
