import sqlite3
import pandas as pd
import plotly.express as px
from scipy.stats import kruskal

def investigate_total_distance_days(conn):
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
        category_orders={'DayOfWeek': day_order},    
    )

    fig.update_traces(marker_color='steelblue')

    fig.update_layout(
        template='plotly_white',
        xaxis_title='Day of the Week',
        yaxis_title='Total Distance',
        showlegend=False, 
        width=800,  
        height=400, 
        margin=dict(l=50, r=50, t=0, b=50),
    )

    return fig