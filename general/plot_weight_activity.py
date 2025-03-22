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
    conn = sqlite3.connect(db_path)

    weight_query = "SELECT Id, Date, WeightKg FROM weight_log"
    activity_query = "SELECT Id, ActivityDate, TotalSteps, Calories FROM daily_activity"

    weight_data = pd.read_sql_query(weight_query, conn)
    activity_data = pd.read_sql_query(activity_query, conn)

    conn.close()

    weight_data["Date"] = pd.to_datetime(weight_data["Date"]).dt.date
    activity_data["ActivityDate"] = pd.to_datetime(activity_data["ActivityDate"]).dt.date

    merged_data = weight_data.merge(
        activity_data,
        left_on=["Id", "Date"],
        right_on=["Id", "ActivityDate"],
        how="inner"
    )

    merged_data.dropna(subset=["WeightKg", "TotalSteps", "Calories"], inplace=True)
    custom_scale = ['lightblue', 'steelblue', 'navy']

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
        color_continuous_scale=custom_scale,
    )

    fig.update_traces(
        marker=dict(
            opacity=1,
            line=dict(width=0.5)
        )
    )

    fig.update_layout(
        width=800,  
        height=400, 
        margin=dict(l=0, r=40, t=0, b=0),
        autosize=False, 
        legend=dict(
            x=0.05,  
            y=0.90, 
            xanchor='left',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )


    return fig
