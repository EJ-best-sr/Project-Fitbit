import pandas as pd
import plotly.graph_objects as go
import sqlite3
import statsmodels.api as sm

def plot_steps_vs_temperature_regression(db_path: str, df_weather: pd.DataFrame):
    """
    Plots a scatter plot with linear regression of Total Steps vs Temperature
    """

    # Load Fitbit data
    conn = sqlite3.connect(db_path)
    df_fitbit = pd.read_sql_query("SELECT ActivityDate AS date, TotalSteps FROM daily_activity", conn)
    df_fitbit["date"] = pd.to_datetime(df_fitbit["date"]).dt.date

    # Prepare weather data
    df_weather = df_weather.copy()
    df_weather["date"] = pd.to_datetime(df_weather["datetime"]).dt.date

    df_merged = pd.merge(df_fitbit, df_weather[["date", "temp"]], on="date", how="inner")

    # Fit linear regression using statsmodels
    X = sm.add_constant(df_merged["temp"])
    model = sm.OLS(df_merged["TotalSteps"], X).fit()
    r_squared = model.rsquared

    # Predict values for regression line
    df_merged["predicted"] = model.predict(X)

    # Create plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_merged["temp"],
        y=df_merged["TotalSteps"],
        mode="markers",
        name="Data Points",
        marker=dict(
            color="rgba(100, 149, 237, 0.6)",  
            size=8,
            line=dict(width=0.5, color='rgba(100, 149, 237, 0.2)'),
            symbol="circle"
        )
    ))

    fig.add_trace(go.Scatter(
        x=df_merged["temp"],
        y=df_merged["predicted"],
        mode="lines",
        name="Regression Line",
        line=dict(color="dimgray", width=3, dash="solid")
    ))

    # Layout styling
    fig.update_layout(
        xaxis_title="Temperature (°F)",
        yaxis_title="Total Steps",
        legend_title="",
        template="plotly_white",
        font=dict(family="Helvetica", size=14, color="black"),
        margin=dict(t=70, b=50, l=60, r=40),
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(bgcolor="rgba(240,240,240,0.8)", bordercolor="gray", borderwidth=1),
        width=800,               
        height=550,  

    )
    return fig, r_squared