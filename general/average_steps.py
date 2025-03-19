import sqlite3
import pandas as pd

conn = sqlite3.connect("fitbit_database.db")

def calculate_average_steps(conn, start_date=None, end_date=None, user_id=None):
    """
    Calculate the average steps for a given user or for all users within a specified date range.

    Parameters:
    - conn: SQLite database connection
    - start_date: (optional) Start date for filtering (format: 'YYYY-MM-DD' or the format in your DB)
    - end_date: (optional) End date for filtering
    - user_id: (optional) The ID of the user

    Returns:
    - The average steps
    """
    query = """
    SELECT AVG(TotalSteps) AS avg_steps
    FROM daily_activity
    WHERE 1=1
    """

    params = []

    # Apply user_id filter if provided
    if user_id:
        query += " AND Id = ?"
        params.append(user_id)

    # Apply date range filter if provided
    if start_date and end_date:
        query += " AND ActivityDate BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    df = pd.read_sql(query, conn, params=params)

    return df["avg_steps"].iloc[0] if not df.empty else 0


#calculate_average_steps(conn, user_id=1503960366)