import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np


def plot_steps_per_4_hour_block():
    """
    Plots the average steps taken per 4-hour time block.

    Data is retrieved from an SQLite database table named 'hourly_steps'.
    The function processes the step data, categorizes it into 4-hour blocks,
    calculates the average steps taken for each block, and visualizes it
    using a Plotly bar chart.

    Parameters:
        None

    Returns:
        plotly.graph_objs._figure.Figure: An interactive bar chart figure
    """
    connection = sqlite3.connect("data/fitbit_database.db")
    query = "SELECT ActivityHour, StepTotal FROM hourly_steps"
    hourly_steps = pd.read_sql_query(query, connection)
    connection.close()
    hourly_steps["ActivityHour"] = pd.to_datetime(hourly_steps["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    hourly_steps["HourBlock"] = hourly_steps["ActivityHour"].dt.hour // 4 * 4
    step_avg = hourly_steps.groupby("HourBlock")["StepTotal"].mean().reset_index()

    # Define labels for the 4-hour blocks
    hour_labels = {0: "0-4am", 4: "4-8am", 8: "8-12pm", 12: "12-4pm", 16: "4-8pm", 20: "8-0am"}
    step_avg["HourBlock"] = step_avg["HourBlock"].map(hour_labels)

    # Find the max value and create a color column
    max_steps = step_avg["StepTotal"].max()
    step_avg["Color"] = np.where(step_avg["StepTotal"] == max_steps, "darkblue", "lightblue")

    # Create the plot
    fig = px.bar(
        step_avg,
        x="HourBlock",
        y="StepTotal",
        color="Color",  # Use the color column
        color_discrete_map={"darkblue": "darkblue", "lightblue": "lightblue"},
        labels={"StepTotal": "Average Steps", "HourBlock": "Time Block"},
        title="Average Steps per 4-Hour Block"
    )

    # Update layout and appearance
    fig.update_layout(
        bargap=0.4,  # Adjust bar gap
        showlegend=False,  # Hide the legend
        xaxis_title='Time Block', 
        yaxis_title='Average Steps',
        title_x=0.5,  # Center the title
    )

    # Optional: Ensure the x-axis is ordered correctly
    hour_block_order = ["0-4am", "4-8am", "8-12pm", "12-4pm", "4-8pm", "8-0am"]
    fig.update_xaxes(categoryorder="array", categoryarray=hour_block_order)

    # Return the figure object
    return fig
