import sqlite3
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go

def analyze_sleep_activity(db_path):
    conn = sqlite3.connect(db_path)
    query_sleep = '''
    SELECT Id, date, value, logId
    FROM minute_sleep
    '''
    df_sleep = pd.read_sql_query(query_sleep, conn)
    df_sleep['date'] = pd.to_datetime(df_sleep['date'])

    df_sleep_grouped = df_sleep.groupby('logId').agg(
        Id=('Id', 'first'), 
        TotalSleepDuration=('value', 'count'),  # Count number of minute entries (each row = 1 min)
        FirstDate=('date', 'min'),  # First date in the logId group (start time)
        LastDate=('date', 'max')  # Last date in the logId group (end time)
    ).reset_index()

    df_sleep_grouped['SleepDate'] = df_sleep_grouped['FirstDate'].dt.date
    df_sleep_grouped['IsMorningSleep'] = (df_sleep_grouped['FirstDate'].dt.hour >= 0) & (df_sleep_grouped['FirstDate'].dt.hour < 11)
    df_sleep_grouped['SleepDate'] = df_sleep_grouped.apply(
        lambda row: (row['FirstDate'] - pd.Timedelta(days=1)).date() if row['IsMorningSleep'] else row['FirstDate'].date(),
        axis=1
    )

    df_sleep_grouped_sorted = pd.concat([group for _, group in df_sleep_grouped.groupby('Id')])
    df_sleep_grouped_sorted = df_sleep_grouped_sorted.reset_index(drop=True)
    df_sleep_aggregated = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
        TotalSleepDuration=('TotalSleepDuration', 'sum') 
    ).reset_index()

    query_activity = '''
    SELECT Id, ActivityDate, 
           (VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) as TotalActiveMinutes
    FROM daily_activity
    '''
    df_activity = pd.read_sql_query(query_activity, conn)
    df_activity['ActivityDate'] = pd.to_datetime(df_activity['ActivityDate']).dt.date


    df_merged = pd.merge(
        df_sleep_aggregated, 
        df_activity, 
        left_on=['Id', 'SleepDate'], 
        right_on=['Id', 'ActivityDate'], 
        how='inner'
    )
    df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]


    X = df_merged_filtered['TotalActiveMinutes']  # Independent variable
    y = df_merged_filtered['TotalSleepDuration']  # Dependent variable
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()


    regression_fig = go.Figure()
    regression_fig.add_trace(
        go.Scatter(
            x=df_merged_filtered['TotalActiveMinutes'],
            y=df_merged_filtered['TotalSleepDuration'],
            mode='markers',
            name='Data Points',
            marker=dict(color='rgba(69, 86, 128, 0.8)', line=dict(color='rgba(69, 86, 128, 0.8)', width=1)),
        )
    )

    predicted = model.predict(X)
    regression_fig.add_trace(
        go.Scatter(
            x=df_merged_filtered['TotalActiveMinutes'],
            y=predicted,
            mode='lines',
            line=dict(color='rgba(0, 0, 0)'),
            name='Regression Line'
        )
    )

    regression_fig.update_layout(
        xaxis_title='Total Active Minutes',
        yaxis_title='Total Sleep Duration',
        showlegend=True,
        template='plotly_white',
        width=800,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        autosize=False,
        legend=dict(
            x=0.80,
            y=0.85,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        ),
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=True, gridcolor='rgba(211, 211, 211, 0.5)')  
    )

    conn.close()

    p_value = model.pvalues['TotalActiveMinutes'] 
    alpha = 0.05
    if p_value < alpha:
        msg = "There is some statistically significant relationship between TotalActiveMinutes and TotalSleepDuration"
    else:
        msg = "There is NO statistically significant relationship between TotalActiveMinutes and TotalSleepDuration"
    info = f"R-squared value is {model.rsquared:.4f} and p-value is {p_value:.4f}. **The model explains {model.rsquared*100:.2f}% of the variation** in TotalSleepDuration based on TotalActiveMinutes. {msg} (significance level is {alpha})."


    return regression_fig, info