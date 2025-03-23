import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

connection = sqlite3.connect("data/fitbit_database.db")

def get_4_hour_sleep_blocks(user_id, date):
    """
    Retrieve and plot the user's sleep data in 4-hour blocks.

    Parameters:
    user_id (float): The user's ID.
    date (str): The date in "MM/DD/YYYY" format.

    Returns:
    pandas.DataFrame: DataFrame with 4-hour blocks and sleep minutes.
    """
    query = "SELECT * FROM minute_sleep WHERE Id = ? AND date LIKE ?"
    df = pd.read_sql_query(query, connection, params=(user_id, f"{date}%"))
    
    df["date"] = pd.to_datetime(df["date"])
    
    # Filter for sleep periods
    df = df[df["value"] >= 1]
    
  # Create a custom function to assign 4-hour blocks
    def get_4_hour_block(hour):
        if 0 <= hour < 4:
            return "0-4"
        elif 4 <= hour < 8:
            return "4-8"
        elif 8 <= hour < 12:
            return "8-12"
        elif 12 <= hour < 16:
            return "12-16"
        elif 16 <= hour < 20:
            return "16-20"
        elif 20 <= hour < 24:
            return "20-0"

    # Apply the function to the 'date' column to get the block label
    df["block"] = df["date"].dt.hour.apply(get_4_hour_block)
    
    # Count sleep minutes per block
    sleep_blocks = df.groupby("block").size().reset_index(name="sleep_minutes")
    
    # Generate the bar plot
    plt.figure(figsize=(10,5))
    plt.bar(sleep_blocks["block"], sleep_blocks["sleep_minutes"])
    plt.xlabel("4-hour blocks")
    plt.ylabel("Sleep minutes")
    plt.title(f"Sleep data for user {user_id} on {date}")
    plt.xticks(rotation=45)
    plt.show()
