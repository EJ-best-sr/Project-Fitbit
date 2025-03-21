import pandas as pd
import numpy as np
import sqlite3

def heart_rate_analysis(user_id):
    """
    Analyzes heart rate variability metrics (RMSSD, SDNN, PNN50) for a given user ID.
    Also calculates average values across all users for comparison.
    
    Parameters:
        user_id (int): The ID of the user whose heart rate data will be analyzed.
    
    Returns:
        pd.DataFrame: A DataFrame containing the calculated metrics and averages.
    """
    # Open the connection inside the function
    connection = sqlite3.connect("data/fitbit_database.db")
    query = f"SELECT * FROM heart_rate WHERE Id = {user_id}"
    heart_rate = pd.read_sql_query(query, connection)

    # Retrieve all data for average calculation
    all_data = pd.read_sql_query("SELECT * FROM heart_rate", connection)
    connection.close()

    if heart_rate.empty:
        return None

    heart_rate['Time'] = pd.to_datetime(heart_rate['Time'])
    heart_rate = heart_rate.sort_values(by='Time')

    # Compute RR intervals (time between heartbeats in milliseconds)
    rr_intervals = 60000 / heart_rate['Value']
    rr_diffs = np.diff(rr_intervals)

    # User-specific metrics
    rmssd = round(np.sqrt(np.mean(rr_diffs**2)), 2)
    sdnn = round(np.std(rr_intervals, ddof=1), 2)
    nn50 = np.sum(np.abs(rr_diffs) > 50)
    pnn50 = round((nn50 / len(rr_diffs)) * 100, 2)

    # Calculate average metrics across all users
    all_rr_intervals = 60000 / all_data['Value']
    all_rr_diffs = np.diff(all_rr_intervals)
    avg_rmssd = round(np.sqrt(np.mean(all_rr_diffs**2)), 2)
    avg_sdnn = round(np.std(all_rr_intervals, ddof=1), 2)
    avg_nn50 = np.sum(np.abs(all_rr_diffs) > 50)
    avg_pnn50 = round((avg_nn50 / len(all_rr_diffs)) * 100, 2)

    # Combine results
    results_df = pd.DataFrame({
        "Metric": ["RMSSD", "SDNN", "PNN50"],
        "User Value": [rmssd, sdnn, pnn50],
        "Average Value*": [avg_rmssd, avg_sdnn, avg_pnn50]
    })

    return results_df

