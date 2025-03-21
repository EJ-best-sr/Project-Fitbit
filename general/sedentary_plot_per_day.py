import sqlite3
import pandas as pd
import plotly.express as px
from scipy.stats import kruskal

def investigate_sedentary_minutes_days(conn):
    query = """
    SELECT ActivityDate, SedentaryMinutes 
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
        y='SedentaryMinutes',
        #title='Distribution of Sedentary Minutes per Day of the Week',
        labels={'DayOfWeek': 'Day of the Week', 'SedentaryMinutes': 'Sedentary Minutes'},
        color='DayOfWeek',  
        category_orders={'DayOfWeek': day_order},  
        color_discrete_sequence=px.colors.qualitative.Pastel 
    )

    fig.update_layout(
        template='plotly_white',
        xaxis_title='Day of the Week',
        yaxis_title='Sedentary Minutes',
        showlegend=False,  
        width=800,  
        height=400,  
        margin=dict(l=50, r=50, t=0, b=50),  
    )

    groups = [df[df['DayOfWeek'] == day]['SedentaryMinutes'] for day in day_order]
    h_stat, p_value = kruskal(*groups)
    print(f"Kruskal-Wallis H-statistic: {h_stat}, p-value: {p_value}")

    return fig