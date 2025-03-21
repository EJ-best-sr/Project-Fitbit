import pandas as pd
import plotly.express as px

def plot_steps_rainy_vs_nonrainy(df_fitbit: pd.DataFrame, df_weather: pd.DataFrame):
    """
    Creates a Plotly boxplot comparing total steps on rainy vs non-rainy days.
    Returns the Plotly figure.
    """
    df_fitbit = df_fitbit.copy()
    df_weather = df_weather.copy()

    df_fitbit['date'] = pd.to_datetime(df_fitbit['date'])
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    df_merged = pd.merge(df_fitbit, df_weather, on="date", how="inner")
    df_merged["Rainy"] = df_merged["precip"] > 0

    fig = px.box(
        df_merged, 
        x="Rainy", 
        y="TotalSteps", 
        labels={"Rainy": "Rainy Day (True/False)", "TotalSteps": "Total Steps"},
        title="Box Plot: Total Steps on Rainy vs Non-Rainy Days"
    )

    return fig