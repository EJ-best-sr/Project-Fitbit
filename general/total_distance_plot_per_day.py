import sqlite3
import pandas as pd
import plotly.graph_objects as go

def investigate_total_distance_days(conn):
    """
    Investigates on which days of the week people cover more total distance using the entire database.
    
    Parameters:
    - conn: SQLite database connection
    
    Returns:
    - fig: A Plotly figure object containing the box plot.
    """
    query = """
    SELECT ActivityDate, TotalDistance 
    FROM daily_activity;
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        print("No activity data found.")
        return None

    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    df['DayOfWeek'] = df['ActivityDate'].dt.strftime('%a') 

    # Reorder days to make sure the plot shows in the correct order
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

    # Create the box plot using Plotly's go.Box
    fig = go.Figure()

    fig.add_trace(go.Box(
        x=df['DayOfWeek'], 
        y=df['TotalDistance'], 
        boxpoints='all',  # Show all points including outliers
        jitter=0.3,  # Slight jitter to avoid overlap
        pointpos=0,  # Position of the points relative to the box
        marker=dict(color='lightblue'),
        name='Total Distance per Day'
    ))

    # Customize layout for better presentation
    fig.update_layout(
        title='Distribution of Total Distance per Day of the Week',
        xaxis_title='Day of the Week',
        yaxis_title='Total Distance (km)',
        boxmode='group',  # Group the box plots by 'DayOfWeek'
        showlegend=False  # Turn off the legend since we don't need it
    )

    # Return the figure object
    return fig
