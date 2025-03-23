import pandas as pd
import numpy as np
import sqlite3

connection = sqlite3.connect("data/fitbit_database.db")

def heart_rate_analysis(user_id):
    """
    Analyzes heart rate variability metrics (RMSSD, SDNN, PNN50) for a given user ID.
    
    Parameters:
        user_id (int): The ID of the user whose heart rate data will be analyzed.
    
    Returns:
        pd.DataFrame: A DataFrame containing the user ID and the calculated metrics.
    """
    query = f"SELECT * FROM heart_rate WHERE Id = {user_id}"
    heart_rate = pd.read_sql_query(query, connection)
    connection.close()
    
    if heart_rate.empty:
        return "No data found for this user."
    
    
    heart_rate['Time'] = pd.to_datetime(heart_rate['Time'])
    heart_rate = heart_rate.sort_values(by='Time')
    
    # Compute RR intervals (time between heartbeats in milliseconds)
    rr_intervals = 60000 / heart_rate['Value']
    # Compute the differences between consecutive RR intervals
    rr_diffs = np.diff(rr_intervals)
    
    # Calculate RMSSD: Root Mean Square of Successive Differences
    rmssd = round(np.sqrt(np.mean(rr_diffs**2)), 2)
    # Calculate SDNN: Standard deviation of all RR intervals
    sdnn = round(np.std(rr_intervals, ddof=1), 2)
    
    # Calculate NN50: Number of successive RR interval differences greater than 50ms
    nn50 = np.sum(np.abs(rr_diffs) > 50)
    # Calculate PNN50: Percentage of NN50 relative to the total RR differences
    pnn50 = round((nn50 / len(rr_diffs)) * 100, 2)
    
    
    results_df = pd.DataFrame({
        "Id": [user_id],
        "RMSSD": [rmssd],
        "SDNN": [sdnn],
        "PNN50": [pnn50]
    })
    
    return results_df
