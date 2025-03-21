import sqlite3
import pandas as pd
from scipy.stats import kruskal

def test_sedentary(conn):
    """
    Do a Kruskal-Wallis test to determine if sedentary minutes significantly differ between days of the week.
    """
    query = """
    SELECT ActivityDate, SedentaryMinutes 
    FROM daily_activity;
    """

    df = pd.read_sql(query, conn)
    if df.empty:
        return None, None 

    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    df['DayOfWeek'] = df['ActivityDate'].dt.strftime('%a') 
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)
    grouped_data = [df[df['DayOfWeek'] == day]['SedentaryMinutes'].dropna().tolist() for day in day_order]
    stat, p_value = kruskal(*grouped_data)

    return stat, p_value
