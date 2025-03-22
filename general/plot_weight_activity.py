import sqlite3
import pandas as pd
import plotly.express as px

def plot_weight_vs_activity(db_path):
    """
    Creates an interactive Plotly scatter plot of:
    Weight (Kg) vs Total Steps, colored and sized by Calories burned.

    Parameters:
    - db_path (str): Path to the SQLite Fitbit database

    Returns:
    - fig (plotly.graph_objs.Figure): The interactive scatter plot
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Load data from tables
    weight_query = "SELECT Id, Date, WeightKg FROM weight_log"
    activity_query = "SELECT Id, ActivityDate, TotalSteps, Calories FROM daily_activity"

    weight_data = pd.read_sql_query(weight_query, conn)
    activity_data = pd.read_sql_query(activity_query, conn)

    conn.close()

    # Convert date formats for merging
    weight_data["Date"] = pd.to_datetime(weight_data["Date"]).dt.date
    activity_data["ActivityDate"] = pd.to_datetime(activity_data["ActivityDate"]).dt.date

    # Merge on Id and date
    merged_data = weight_data.merge(
        activity_data,
        left_on=["Id", "Date"],
        right_on=["Id", "ActivityDate"],
        how="inner"
    )

    # Drop missing values
    merged_data.dropna(subset=["WeightKg", "TotalSteps", "Calories"], inplace=True)

    # Plotly scatter plot with bubble size & color for calories
    fig = px.scatter(
        merged_data,
        x="TotalSteps",
        y="WeightKg",
        color="Calories",
        size="Calories",
        hover_data=["Id", "Date"],
        labels={
            "TotalSteps": "Total Steps",
            "WeightKg": "Weight (Kg)",
            "Calories": "Calories Burned"
        },
        template="plotly_white",
        color_continuous_scale="Viridis",
    )

    return fig
