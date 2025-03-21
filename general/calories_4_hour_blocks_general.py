import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

def plot_calories_per_4_hour_block():
    """
    Plots the average calories burnt per 4-hour time block.

    Data is retrieved from an SQLite database table named 'hourly_calories'.
    The function processes the calorie data, categorizes it into 4-hour blocks,
    calculates the average calories burnt for each block, and visualizes it
    using a Plotly bar chart.

    Returns:
        plotly.graph_objs._figure.Figure: An interactive bar chart showing average calories burnt per 4-hour block.
    """
    connection = sqlite3.connect("data/fitbit_database.db")
    query = "SELECT ActivityHour, Calories FROM hourly_calories"
    hourly_calories = pd.read_sql_query(query, connection)
    connection.close()

    hourly_calories["ActivityHour"] = pd.to_datetime(
        hourly_calories["ActivityHour"], 
        format="%m/%d/%Y %I:%M:%S %p", 
        errors="coerce"
    )
    hourly_calories["HourBlock"] = hourly_calories["ActivityHour"].dt.hour // 4 * 4

    calories_avg = hourly_calories.groupby("HourBlock")["Calories"].mean().reset_index()

    hour_labels = {
        0: "0-4am", 4: "4-8am", 8: "8-12pm",
        12: "12-4pm", 16: "4-8pm", 20: "8-0am"
    }
    calories_avg["HourBlock"] = calories_avg["HourBlock"].map(hour_labels)

    # Define the custom order for the hour blocks
    hour_block_order = ["0-4am", "4-8am", "8-12pm", "12-4pm", "4-8pm", "8-0am"]

    # Find the max value and create a color column
    max_calories = calories_avg["Calories"].max()
    calories_avg["Color"] = np.where(calories_avg["Calories"] == max_calories, "darkblue", "lightblue")

    # Plotting the figure with correct category order
    fig = px.bar(
        calories_avg, 
        x="HourBlock", 
        y="Calories", 
        color="Color",  # Use the color column
        color_discrete_map={"darkblue": "darkblue", "lightblue": "lightblue"},
        labels={"Calories": "Average Calories Burnt", "HourBlock": "Time Block"},
        category_orders={"HourBlock": hour_block_order}# Set custom order for the x-axis
    )

    fig.update_layout(bargap=0.4, showlegend=False)

    return fig

    fig.update_layout(bargap=0.4, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))

    return fig
