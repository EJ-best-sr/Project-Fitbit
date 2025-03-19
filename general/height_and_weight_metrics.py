import sqlite3
import pandas as pd
import numpy as np


def replace_missing_values_weight_log(db_path):
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
    connection = sqlite3.connect(db_path)
    query = "SELECT * FROM weight_log"
    weight_data = pd.read_sql_query(query, connection).set_index("Id")
    connection.close()
    weight_data_copy = weight_data.copy()
    weight_data_copy["WeightKg"].fillna(weight_data_copy["WeightPounds"] * 0.45359237, inplace=True)
    return weight_data_copy

def add_height_column(weight_data_copy):
    """
    Adds a column 'Height' to the DataFrame, calculated from the BMI and Weight.

    Parameters:
        weight_data_copy (pd.DataFrame): The DataFrame containing weight and BMI columns.

    Returns:
        pd.DataFrame: The DataFrame with the added 'Height' column.
    """
    # Bereken de hoogte op basis van de BMI en het gewicht
    # Formule: Height = sqrt(Weight / BMI)
    weight_data_copy['Height'] = np.sqrt(weight_data_copy['WeightKg'] / weight_data_copy['BMI'])
    
    # Return een kopie van de DataFrame met de nieuwe 'Height' kolom
    return weight_data_copy.copy()

