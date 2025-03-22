import sqlite3
import pandas as pd
import plotly.express as px

def plot_fitbit_usage_pie(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT Id, ActivityDate FROM daily_activity"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
    days_used = df.groupby('Id')['ActivityDate'].nunique().reset_index()
    days_used.columns = ['Id', 'DaysUsed']

    def categorize_days(days):
        if days <= 10:
            return '1–10 Days'
        elif days <= 21:
            return '11–21 Days'
        else:
            return '22–32 Days'

    days_used['UsageGroup'] = days_used['DaysUsed'].apply(categorize_days)

    usage_counts = days_used['UsageGroup'].value_counts().reset_index()
    usage_counts.columns = ['Usage Group', 'Count']

    fig = px.pie(
        usage_counts,
        values='Count',
        names='Usage Group',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textinfo='percent+label')

    fig.update_layout(
        showlegend=True,
        template='plotly_white',
        width=800,  
        height=400,  
        margin=dict(l=0, r=50, t=50, b=0), 
        legend=dict(
            title="Usage Groups",
            font=dict(size=14),         
            bgcolor='rgba(255, 255, 255, 0.5)',  
            bordercolor='black',          
            borderwidth=1,               
            x=0.80,                        
            y=0.80,                       
        )  
    )  


    return fig