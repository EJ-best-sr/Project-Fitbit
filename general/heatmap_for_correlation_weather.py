import pandas as pd
import plotly.graph_objects as go
import sqlite3
def combined_weather_fitbit_heatmap(weather_df: pd.DataFrame, conn: sqlite3.Connection) -> go.Figure:
     # Load Fitbit data
    activity_df = pd.read_sql_query("SELECT * FROM daily_activity", conn)
    activity_df["ActivityDate"] = pd.to_datetime(activity_df["ActivityDate"]).dt.date
    activity_metrics = activity_df[[
        "ActivityDate", "Calories", "TotalSteps", "VeryActiveMinutes", "LightlyActiveMinutes"
    ]]

    sleep_df = pd.read_sql_query("SELECT * FROM minute_sleep", conn)
    sleep_df["date"] = pd.to_datetime(sleep_df["date"]).dt.date
    sleep_daily = sleep_df[sleep_df["value"] == 1].groupby("date").size().reset_index(name="TotalSleepDuration")

    weight_df = pd.read_sql_query("SELECT * FROM weight_log", conn)
    weight_df["Date"] = pd.to_datetime(weight_df["Date"]).dt.date
    weight_daily = weight_df.groupby("Date")["WeightKg"].mean().reset_index()

    # Merge Fitbit parts
    fitbit = activity_metrics.merge(sleep_daily, left_on="ActivityDate", right_on="date", how="left")
    fitbit = fitbit.merge(weight_daily, left_on="ActivityDate", right_on="Date", how="left")
    fitbit = fitbit.drop(columns=["date", "Date"])

    # Merge with weather
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"]).dt.date
    weather = weather_df[["datetime", "temp", "humidity", "precip", "feelslikemax", "windgust"]]

    merged = pd.merge(fitbit, weather, left_on="ActivityDate", right_on="datetime", how="inner")
    merged = merged.select_dtypes(include="number")

    corr = merged.corr(method="pearson")
    fitbit_features = ["Calories", "TotalSteps", "VeryActiveMinutes", "LightlyActiveMinutes", "TotalSleepDuration", "WeightKg"]
    weather_features = ["temp", "humidity", "precip", "feelslikemax", "windgust"]
    sub_corr = corr.loc[weather_features, fitbit_features]

    fig = go.Figure(data=go.Heatmap(
        z=sub_corr.values,
        x=sub_corr.columns,
        y=sub_corr.index,
        colorscale="RdBu",
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Pearson Correlation")
    ))

    fig.update_layout(
        xaxis_title="Fitbit Metrics",
        yaxis_title="Weather Metrics",
        template="plotly_white",
        width=800,               
        height=550,             
    )

    return fig