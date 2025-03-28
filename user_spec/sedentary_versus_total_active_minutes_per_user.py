import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

def plot_active_sedentary_minutes_daily(conn, user_id, start_date, end_date):
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
        print(f"No activity data found between {start_date.strftime('%m/%d/%Y')} and {end_date.strftime('%m/%d/%Y')}.")
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
        line=dict(color="rgba(147, 112, 219, 0.8)", width=4),
        marker=dict(symbol='circle', size=8)
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered['ActivityDate'],
        y=df_filtered['SedentaryMinutes'],
        mode='lines+markers',
        name='Sedentary Minutes',
        line=dict(color="rgba(72, 61, 139, 0.8)", width=4),
        marker=dict(symbol='circle', size=8)
    ))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Minutes',
        legend=dict(
            title="Metrics",
            x=1.02,  
            y=1,     
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.7)',  
            font=dict(size=12),
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1  
        ),
        template="plotly_white",
        height=400, 
        width = 800,
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=False

    )

    return fig