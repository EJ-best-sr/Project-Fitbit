import sqlite3
import pandas as pd
import plotly.express as px

def plot_sleep_vs_weight(db_path):
    import sqlite3
    import pandas as pd
    import plotly.express as px

    conn = sqlite3.connect(db_path)

    # Load and filter sleep data to keep only 'asleep' minutes
    sleep_df = pd.read_sql_query("SELECT Id, date, value FROM minute_sleep", conn)
    sleep_df = sleep_df[sleep_df['value'] == 1].copy()
    sleep_df['date'] = pd.to_datetime(sleep_df['date'])

    # Count total minutes asleep per user per day
    daily_sleep = sleep_df.groupby(['Id', sleep_df['date'].dt.date]).size().reset_index(name='TotalMinutesAsleep')
    daily_sleep.columns = ['Id', 'Date', 'TotalMinutesAsleep']
    daily_sleep['Date'] = pd.to_datetime(daily_sleep['Date'])

    # Load weight data
    weight_df = pd.read_sql_query("SELECT Id, Date, WeightKg FROM weight_log", conn)
    weight_df['Date'] = pd.to_datetime(weight_df['Date'])

    conn.close()

    # Merge: closest date per user
    merged_df = pd.merge_asof(
        daily_sleep.sort_values("Date"),
        weight_df.sort_values("Date"),
        on="Date",
        by="Id",
        direction='nearest',
        tolerance=pd.Timedelta(days=2)
    )

    merged_df.dropna(subset=['WeightKg', 'TotalMinutesAsleep'], inplace=True)

    # Convert to hours
    merged_df['SleepHours'] = merged_df['TotalMinutesAsleep'] / 60

    # Bubble plot
    fig = px.scatter(
        merged_df,
        x="WeightKg",
        y="SleepHours",
        size="SleepHours",
        color="SleepHours",
        color_continuous_scale="Blues",
        labels={"WeightKg": "Weight (kg)", "SleepHours": "Sleep Duration (hours)"},
        template="plotly_white"
    )

    fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(coloraxis_colorbar=dict(title="Sleep (hrs)"))

    return fig