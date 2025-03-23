import sqlite3
import pandas as pd
import plotly.graph_objects as go

def plot_fitbit_usage_pie(db_path):
    # Connect to the database and fetch data
    conn = sqlite3.connect(db_path)
    query = "SELECT Id, ActivityDate FROM daily_activity"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert ActivityDate to datetime and calculate unique days used per user
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
    days_used = df.groupby('Id')['ActivityDate'].nunique().reset_index()
    days_used.columns = ['Id', 'DaysUsed']

    # Categorize days used
    def categorize_days(days):
        if days <= 10:
            return '1–10 Days'
        elif days <= 21:
            return '11–21 Days'
        else:
            return '22–32 Days'

    days_used['UsageGroup'] = days_used['DaysUsed'].apply(categorize_days)

    # Count usage groups
    usage_counts = days_used['UsageGroup'].value_counts().reset_index()
    usage_counts.columns = ['Usage Group', 'Count']

    # Define the desired order of categories
    category_order = ['1–10 Days', '11–21 Days', '22–32 Days']
    usage_counts['Usage Group'] = pd.Categorical(usage_counts['Usage Group'], categories=category_order, ordered=True)
    usage_counts = usage_counts.sort_values('Usage Group')

    # Extract labels and values in the desired order
    labels = usage_counts['Usage Group'].tolist()
    values = usage_counts['Count'].tolist()

    # Define colors
    colors = [
        'rgba(32, 178, 170, 0.5)',
        'rgba(0, 128, 128, 0.65)' ,
        'rgba(11, 97, 107, 0.9)'   
    ]

    # Define font sizes
    font_sizes = [40 if label == "11–21 Days" else 16 for label in labels]

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hoverinfo="label+percent",
        textinfo="percent",
        insidetextorientation="horizontal",
        textfont=dict(color="white", size=font_sizes),
        marker=dict(colors=colors),
        sort=False  # Disable automatic sorting of the pie chart
    )])

    # Update layout
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
            traceorder='normal'  # Ensure the legend follows the order of the data
        )
    )

    return fig