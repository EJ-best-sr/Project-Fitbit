import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_weight_vs_factors(db_path):
    """
    Creates interactive Plotly scatter plots with trend lines showing relationships between:
    - Weight vs Steps
    - Weight vs Calories
    - Weight vs Sleep
    - Weight vs Heart Rate

    Parameters:
    - db_path (str): Path to the SQLite Fitbit database

    Returns:
    - figs (list of plotly.graph_objs.Figure): List of 4 regression plots
    """
    conn = sqlite3.connect(db_path)

    # Load data
    activity = pd.read_sql_query("""
        SELECT Id, ActivityDate, TotalSteps, Calories, SedentaryMinutes, VeryActiveMinutes, LightlyActiveMinutes
        FROM daily_activity
    """, conn)

    weight = pd.read_sql_query("SELECT Id, Date, WeightKg FROM weight_log", conn)
    sleep = pd.read_sql_query("SELECT Id, AVG(value) AS AvgSleepMinutes FROM minute_sleep GROUP BY Id", conn)
    heartrate = pd.read_sql_query("SELECT Id, AVG(value) AS AvgHeartRate FROM heart_rate GROUP BY Id", conn)

    conn.close()

    # Preprocess
    activity["ActivityDate"] = pd.to_datetime(activity["ActivityDate"]).dt.date
    weight["Date"] = pd.to_datetime(weight["Date"]).dt.date
    merged = activity.merge(weight, left_on=["Id", "ActivityDate"], right_on=["Id", "Date"], how="outer")
    merged.sort_values(by=["Id", "ActivityDate"], inplace=True)
    merged["WeightKg"] = merged.groupby("Id")["WeightKg"].transform(lambda x: x.interpolate(method="linear"))

    # Summary
    summary = merged.groupby("Id", as_index=False).agg(
        AvgSteps=("TotalSteps", "mean"),
        AvgCalories=("Calories", "mean"),
        AvgSedentaryMinutes=("SedentaryMinutes", "mean"),
        AvgVeryActiveMinutes=("VeryActiveMinutes", "mean"),
        AvgLightlyActiveMinutes=("LightlyActiveMinutes", "mean"),
        AvgWeight=("WeightKg", "mean")
    )

    # Merge with sleep and heart rate
    summary = summary.merge(sleep, on="Id", how="outer")
    summary = summary.merge(heartrate, on="Id", how="outer")

    # Fill missing sleep and heart rate with medians
    summary["AvgSleepMinutes"] = summary["AvgSleepMinutes"].fillna(summary["AvgSleepMinutes"].median())
    summary["AvgHeartRate"] = summary["AvgHeartRate"].fillna(summary["AvgHeartRate"].median())
    summary = summary.dropna(subset=["AvgWeight"])

    # Helper for regression plots
    def make_regression_plot(x, y, xlabel, ylabel, title):
        fig = px.scatter(summary, x=x, y=y, trendline="ols", labels={x: xlabel, y: ylabel})
        fig.update_layout(title=title, template="plotly_white")
        return fig

    # Create all four plots
    fig_steps = make_regression_plot("AvgSteps", "AvgWeight", "Average Steps", "Average Weight (Kg)", "Steps vs Weight")
    fig_calories = make_regression_plot("AvgCalories", "AvgWeight", "Average Calories", "Average Weight (Kg)", "Calories vs Weight")
    fig_sleep = make_regression_plot("AvgSleepMinutes", "AvgWeight", "Average Sleep Minutes", "Average Weight (Kg)", "Sleep vs Weight")
    fig_hr = make_regression_plot("AvgHeartRate", "AvgWeight", "Average Heart Rate", "Average Weight (Kg)", "Heart Rate vs Weight")

    return [fig_steps, fig_calories, fig_sleep, fig_hr]
