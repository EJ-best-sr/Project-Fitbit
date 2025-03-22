import pandas as pd
import plotly.express as px
import sqlite3
import statsmodels.api as sm

def plot_steps_vs_temperature_regression(db_path: str, df_weather: pd.DataFrame):
    """
    Plots a scatter plot with linear regression of Total Steps vs Temperature,
    and includes the R² value in the chart title.
    """
    # Load Fitbit steps
    conn = sqlite3.connect(db_path)
    df_fitbit = pd.read_sql_query("SELECT ActivityDate AS date, TotalSteps FROM daily_activity", conn)
    df_fitbit["date"] = pd.to_datetime(df_fitbit["date"]).dt.date

    # Prepare weather
    df_weather = df_weather.copy()
    df_weather["date"] = pd.to_datetime(df_weather["datetime"]).dt.date

    df_merged = pd.merge(df_fitbit, df_weather[["date", "temp"]], on="date", how="inner")

    X = sm.add_constant(df_merged["temp"])
    model = sm.OLS(df_merged["TotalSteps"], X).fit()
    r_squared = model.rsquared

    fig = px.scatter(
        df_merged,
        x="temp",
        y="TotalSteps",
        trendline="ols",
        labels={"temp": "Temperature (°F)", "TotalSteps": "Total Steps"},
    )

    return fig