import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

connection = sqlite3.connect("data/fitbit_database.db")

def plot_total_distance_per_day(user_id, start_date, end_date):
    """
    Plots total distance per day for a given user within a specified date range.

    Parameters:
        user_id (int): The ID of the user.
        start_date (str): The start date in the format 'MM/DD/YYYY'.
        end_date (str): The end date in the format 'MM/DD/YYYY'.

    Returns:
        None (Displays a bar plot of total distance per day for the user)
    """
    query = f"""
    SELECT ActivityDate, TotalDistance
    FROM daily_activity
    WHERE Id = {user_id} 
    AND ActivityDate BETWEEN '{start_date}' AND '{end_date}'
    """
    total_distance = pd.read_sql_query(query, connection)
    total_distance['ActivityDate'] = pd.to_datetime(total_distance['ActivityDate'])
    plt.figure(figsize=(14, 7))
    sns.barplot(data=total_distance, x='ActivityDate', y='TotalDistance')
    plt.title(f"Total Distance per Day for User {user_id} from {start_date} to {end_date}", fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Total Distance (km)', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()
