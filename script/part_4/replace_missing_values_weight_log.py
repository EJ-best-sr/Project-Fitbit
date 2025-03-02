import sqlite3
import pandas as pd

connection = sqlite3.connect("data/fitbit_database.db")

def replace_missing_values_weight_log():
    """
    Retrieves the 'weight_log' table from the database, replaces missing values in the 'WeightKg' column 
    with the equivalent weight in kilograms based on the 'WeightPounds' column, and returns a copy of the 
    modified data without altering the original database.

    Parameters:
    None

    Returns:
    pd.DataFrame: A copy of the 'weight_log' table with updated 'WeightKg' values where NaN values are 
                  replaced by the conversion from 'WeightPounds' to 'WeightKg'.
    """
    query = "SELECT * FROM weight_log"
    weight_data = pd.read_sql_query(query, connection).set_index("Id")
    weight_data_copy = weight_data.copy()
    weight_data_copy["WeightKg"].fillna(weight_data_copy["WeightPounds"] * 0.45359237, inplace=True)
    return weight_data_copy
