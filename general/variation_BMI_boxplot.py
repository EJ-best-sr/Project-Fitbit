import sqlite3
import pandas as pd
import plotly.express as px

def plot_bmi_weight_boxplots(db_path):
    """
    Generates two Plotly box plots:
    1. BMI variations by user class
    2. Weight variations by user class

    Parameters:
    - db_path (str): Path to the SQLite Fitbit database

    Returns:
    - fig_bmi (plotly.graph_objs.Figure)
    - fig_weight (plotly.graph_objs.Figure)
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Classify users based on their activity count
    user_class_query = """
        SELECT Id, 
               CASE 
                   WHEN COUNT(ActivityDate) <= 10 THEN 'Light User'
                   WHEN COUNT(ActivityDate) BETWEEN 11 AND 15 THEN 'Moderate User'
                   ELSE 'Heavy User'
               END AS Class
        FROM daily_activity
        GROUP BY Id
    """
    user_classification_df = pd.read_sql_query(user_class_query, conn)

    # Load weight_log table
    weight_log = pd.read_sql_query("SELECT Id, WeightKg, BMI FROM weight_log", conn)

    # Close connection
    conn.close()

    # Merge classification with weight data
    merged_data = weight_log.merge(user_classification_df, on="Id", how="left")

    # Box Plot: BMI by Class
    fig_bmi = px.box(
        merged_data,
        x="Class",
        y="BMI",
        color="Class",
        title="BMI Variations by User Class",
        labels={"Class": "User Classification", "BMI": "BMI"},
        template="plotly_white"
    )

    # Box Plot: Weight by Class
    fig_weight = px.box(
        merged_data,
        x="Class",
        y="WeightKg",
        color="Class",
        title="Weight Variations by User Class",
        labels={"Class": "User Classification", "WeightKg": "Weight (Kg)"},
        template="plotly_white"
    )

    return fig_bmi, fig_weight