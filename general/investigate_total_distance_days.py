import sqlite3
import pandas as pd
import plotly.express as px
from scipy.stats import kruskal

def investigate_total_distance_days(conn):
    """
    Investigate on which days of the week people cover more total distance using the entire database.
    
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
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

    fig = px.box(
        df,
        x='DayOfWeek',
        y='TotalDistance',
        #title='Distribution of Total Distance per Day of the Week',
        labels={'DayOfWeek': 'Day of the Week', 'TotalDistance': 'Total Distance'},
        color='DayOfWeek',  # Color by day of the week
        category_orders={'DayOfWeek': day_order},  # Ensure correct order of days
        color_discrete_sequence=px.colors.qualitative.Pastel  # Use a pastel color scheme
    )

    fig.update_layout(
        template='plotly_white',
        xaxis_title='Day of the Week',
        yaxis_title='Total Distance',
        showlegend=False, 
        width=800,  
        height=400, 
        margin=dict(l=50, r=50, t=0, b=50),
    )

    # Perform Kruskal-Wallis test to check for significant differences
    groups = [df[df['DayOfWeek'] == day]['TotalDistance'] for day in day_order]
    h_stat, p_value = kruskal(*groups)
    print(f"Kruskal-Wallis H-statistic: {h_stat}, p-value: {p_value}")

    return fig