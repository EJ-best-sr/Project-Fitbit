import sqlite3
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def plot_activity_distribution(conn, user_id=None):
    """
    Plots a pie chart showing the percentage distribution of 
    LightlyActiveMinutes, FairlyActiveMinutes, and VeryActiveMinutes.
    If a user ID is provided, the chart will display data for that user only; 
    otherwise, it uses the entire database.

    Parameters:
    - conn: SQLite database connection
    - user_id: The ID of the user for specific analysis (default: None)
    
    Returns:
    - fig: A Plotly figure object containing the pie chart
    """
    
    # If a user_id is specified, filter the data for the specific user
    if user_id:
        query = """
        SELECT SUM(LightlyActiveMinutes) AS LightlyActive,
               SUM(FairlyActiveMinutes) AS FairlyActive,
               SUM(VeryActiveMinutes) AS VeryActive
        FROM daily_activity
        WHERE Id = ?;
        """
        df = pd.read_sql(query, conn, params=(user_id,))
    else:
        # Otherwise, use the entire database
        query = """
        SELECT SUM(LightlyActiveMinutes) AS LightlyActive,
               SUM(FairlyActiveMinutes) AS FairlyActive,
               SUM(VeryActiveMinutes) AS VeryActive
        FROM daily_activity;
        """
        df = pd.read_sql(query, conn)

    active_minutes = df.iloc[0].tolist()
    labels = ["Lightly Active", "Very Active", "Fairly Active"]
    colors = ["#c5e6fc", "#1f77b4", "#78b4de"]

    # Check if there is activity data available
    if sum(active_minutes) == 0 or any(pd.isnull(active_minutes)):
        st.warning("⚠️ No activity data found in the database.")
        return None

    # Custom font sizes: Increase the size for Lightly Active
    font_sizes = [20 if label == "Lightly Active" else 14 for label in labels]

    # Create the pie chart using Plotly
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=active_minutes, 
        hoverinfo="label+percent", 
        textinfo="percent", 
        insidetextorientation="horizontal",  # Keep text inside
        textfont=dict(color="white", size=font_sizes),  # White text, larger size for Lightly Active
        marker=dict(colors=colors)
    )])

    # Update the layout of the figure
    fig.update_layout(
        title="Activity Minutes Distribution" + (" for User " + str(user_id) if user_id else " in Database"),
        title_x=0.5
    )

    return fig

# Example usage in Streamlit

