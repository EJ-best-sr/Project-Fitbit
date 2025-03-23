import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

connection = sqlite3.connect("data/fitbit_database.db")

def plot_total_steps_per_day(user_id, start_date, end_date):
    """
    Plots total steps per day for a given user within a specified date range.

    Parameters:
        user_id (int): The ID of the user.
        start_date (str): The start date in the format 'MM/DD/YYYY'.
        end_date (str): The end date in the format 'MM/DD/YYYY'.

    Returns:
        None (Displays a bar plot of total steps per day for the user)
    """
    query = f"""
    SELECT ActivityDate, TotalSteps
    FROM daily_activity
    WHERE Id = {user_id} 
    AND ActivityDate BETWEEN '{start_date}' AND '{end_date}'
    """
    total_steps = pd.read_sql_query(query, connection)
    total_steps['ActivityDate'] = pd.to_datetime(total_steps['ActivityDate'])
    plt.figure(figsize=(14, 7))
    sns.barplot(data=total_steps, x='ActivityDate', y='TotalSteps')
    plt.title(f"Total Steps per Day for User {user_id} from {start_date} to {end_date}", fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Total Steps', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()
