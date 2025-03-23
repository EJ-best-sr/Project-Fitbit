import sqlite3
import pandas as pd

def interpolate_weight_per_user():
    """
    Fetches weight and activity data, interpolates missing weight values, 
    and prepares the dataset for performance analysis.
    
    Returns:
    pd.DataFrame: A DataFrame with estimated weight values for each day.
    """
    # Connect to the database
    conn = sqlite3.connect("fitbit_database.db")

    # Fetch weight data
    weight_query = """
        SELECT Id, Date, WeightKg 
        FROM weight_log
    """
    weight_data = pd.read_sql_query(weight_query, conn)

    # Fetch daily activity data
    activity_query = """
        SELECT Id, ActivityDate, TotalSteps, Calories
        FROM daily_activity
    """
    activity_data = pd.read_sql_query(activity_query, conn)

    # Close the connection
    conn.close()

    # Convert dates to datetime
    weight_data["Date"] = pd.to_datetime(weight_data["Date"]).dt.date
    activity_data["ActivityDate"] = pd.to_datetime(activity_data["ActivityDate"]).dt.date

    # Merge activity with weight data
    merged_data = activity_data.merge(weight_data, left_on=["Id", "ActivityDate"], right_on=["Id", "Date"], how="left")

    # Sort by user and date for proper interpolation
    merged_data = merged_data.sort_values(by=["Id", "ActivityDate"])

    # Interpolate missing weight values for each user
    merged_data["WeightKg"] = merged_data.groupby("Id")["WeightKg"].apply(lambda group: group.interpolate(method="linear"))

    return merged_data

# Generate interpolated dataset
interpolated_data = interpolate_weight_per_user()

# Display first few rows
import ace_tools as tools
tools.display_dataframe_to_user(name="Interpolated Weight and Activity Data", dataframe=interpolated_data)