import pandas as pd
import plotly.express as px

def plot_corr_weather_vs_steps(df_fitbit: pd.DataFrame, df_weather: pd.DataFrame):
    """
    Creates a Plotly bar chart of correlation between weather variables and total steps.
    Returns the Plotly figure.
    """
    df_fitbit = df_fitbit.copy()
    df_weather = df_weather.copy()

    df_fitbit['date'] = pd.to_datetime(df_fitbit['date'])
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    df_merged = pd.merge(df_fitbit, df_weather, on="date", how="inner")
    weather_factors = ["temp", "humidity", "precip", "windspeed"]

    corr = df_merged[weather_factors + ["TotalSteps"]].corr()["TotalSteps"].drop("TotalSteps")
    df_corr = corr.reset_index()
    df_corr.columns = ["Weather Factor", "Correlation with Steps"]

    fig = px.bar(
        df_corr,
        x="Weather Factor",
        y="Correlation with Steps",
        title="Correlation of Weather Factors with Total Steps",
        labels={"Correlation with Steps": "Correlation"},
        color="Correlation with Steps",
        color_continuous_scale="Blues"
    )

    return fig