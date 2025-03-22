import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

def plot_sleep_per_4_hour_block():
    """
    Plots the average minutes of sleep per 4-hour time block.

    Data is retrieved from an SQLite database table named 'minute_sleep'.
    The function processes the sleep data, categorizes it into 4-hour blocks,
    calculates the average sleep duration for each block, and visualizes it
    using a Plotly bar chart.

    Parameters:
        None

    Returns:
        plotly.graph_objs._figure.Figure: An interactive bar chart figure
    """
    connection = sqlite3.connect("data/fitbit_database.db")

    query = "SELECT date, value, logId FROM minute_sleep"
    minute_sleep = pd.read_sql_query(query, connection)

    connection.close()

    minute_sleep["date"] = pd.to_datetime(minute_sleep["date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    minute_sleep["HourBlock"] = (minute_sleep["date"].dt.hour // 4) * 4
    
    sleep_count = minute_sleep[minute_sleep["value"] > 0].groupby(["logId", "HourBlock"])["value"].count().reset_index()
    sleep_avg = sleep_count.groupby("HourBlock")["value"].mean().reset_index()

    hour_labels = {
    0: "0-4am", 
    4: "4-8am", 
    8: "8-12pm", 
    12: "12-4pm", 
    16: "4-8pm", 
    20: "8-0am"
    }
    sleep_avg["HourBlock"] = sleep_avg["HourBlock"].map(hour_labels)


    max_sleep = sleep_avg["value"].max()
    sleep_avg["Color"] = np.where(sleep_avg["value"] == max_sleep, "slategray", "steelblue")

    fig = px.bar(
        sleep_avg,
        x="HourBlock",
        y="value",
        color="Color",
        color_discrete_map={"slategray": "slategray", "steelblue": "steelblue"},
        labels={"value": "Average Minutes Asleep", "HourBlock": "Time Block"}
    )

    fig.update_layout(
        bargap=0.4,
        showlegend=False,
        xaxis_title='Time Block', 
        yaxis_title='Average Minutes Asleep',
        margin=dict(l=0, r=0, t=0, b=0)
    )

    hour_block_order = ["0-4am", "4-8am", "8-12pm", "12-4pm", "4-8pm", "8-0am"]
    fig.update_xaxes(categoryorder="array", categoryarray=hour_block_order)

    return fig
