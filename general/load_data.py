import pandas as pd
import datetime as dt

def load_data(file_path):
    """
    Loads activity data from a CSV file and converts the 'ActivityDate' column to datetime format.

    Parameters:
        file_path (str): The path to the CSV file containing activity data.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded activity data with 'ActivityDate' as a datetime object.
    """
    df = pd.read_csv(file_path)
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    return df
