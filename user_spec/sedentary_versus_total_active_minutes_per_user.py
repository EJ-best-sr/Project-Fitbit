import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

def plot_active_sedentary_minutes_daily(conn, user_id, start_date, end_date):
    """
    Plot Total Active Minutes (sum of VeryActive, FairlyActive, and LightlyActive minutes)
    and Sedentary Minutes for each day from a start date to an end date for a specific user.
    Display dates as month/day and include the shortened day of the week on the x-axis.
    
    Parameters:
    - conn: SQLite database connection
    - user_id: The ID of the user to analyze
    - start_date: Start date for the analysis (format: 'M/D/YYYY' or 'MM/DD/YYYY')
    - end_date: End date for the analysis (format: 'M/D/YYYY' or 'MM/DD/YYYY')
    
    Returns:
    - fig: A Plotly figure object containing the plot.
    """

    query = """
    SELECT ActivityDate, VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes, SedentaryMinutes 
    FROM daily_activity
    WHERE Id = ?;
    """

    df = pd.read_sql(query, conn, params=(user_id,))

    if df.empty:
        print(f"No activity data found.")
        return None

    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    df_filtered = df[(df['ActivityDate'] >= start_date) & (df['ActivityDate'] <= end_date)]

    if df_filtered.empty:
        print(f"⚠️ No activity data found for user {user_id} between {start_date.strftime('%m/%d/%Y')} and {end_date.strftime('%m/%d/%Y')}.")
        return None

    df_filtered['TotalActiveMinutes'] = (
        df_filtered['VeryActiveMinutes'] +
        df_filtered['FairlyActiveMinutes'] +
        df_filtered['LightlyActiveMinutes']
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtered['ActivityDate'],
        y=df_filtered['TotalActiveMinutes'],
        mode='lines+markers',
        name='Total Active Minutes',
        line=dict(color='blue'),
        marker=dict(symbol='circle')
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered['ActivityDate'],
        y=df_filtered['SedentaryMinutes'],
        mode='lines+markers',
        name='Sedentary Minutes',
        line=dict(color='red'),
        marker=dict(symbol='circle')
    ))

    fig.update_layout(
        # title=f'Total Active Minutes vs Sedentary Minutes by Day\n from {start_date.strftime("%m/%d/%Y")} to {end_date.strftime("%m/%d/%Y")}',
        xaxis_title='Date',
        yaxis_title='Minutes',
        xaxis=dict(
            tickmode='array',
            tickvals=df_filtered['ActivityDate'],
            ticktext=[f"{date.strftime('%m/%d')}\n{date.strftime('%a')}" for date in df_filtered['ActivityDate']],
            tickangle=45
        ),
        legend=dict(
            x=0.8,  
            y=0.9,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.7)',  
            font=dict(size=12),
            borderwidth=1  
        ),
        template="plotly_white",
    )

    return fig
