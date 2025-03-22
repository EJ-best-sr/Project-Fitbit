import pandas as pd
import plotly.graph_objects as go

def plot_precipitation_chart(data: pd.DataFrame):
    """
    Plot daily precipitation as bars and cumulative precipitation as an area chart.

    Parameters:
    - data (pd.DataFrame): Must contain 'datetime' and 'precip' columns.
    """
    df = data.copy()

    # Ensure datetime is in datetime format
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")

    # Fill missing values and compute cumulative precipitation
    df["precip"] = df["precip"].fillna(0)
    df["precip_cumulative"] = df["precip"].cumsum()

    # Plot using Plotly
    fig = go.Figure()

    # Bar chart: daily precipitation
    fig.add_trace(go.Bar(
        x=df["datetime"],
        y=df["precip"],
        name="Precipitation",
        marker_color="darkblue"
    ))

    # Area chart: cumulative precipitation
    fig.add_trace(go.Scatter(
        x=df["datetime"],
        y=df["precip_cumulative"],
        name="Total",
        mode="lines",
        fill="tozeroy",
        line=dict(color="lightgreen")
    ))

    # Layout styling
    fig.update_layout(
        title="Daily and Cumulative Precipitation",
        xaxis_title="Date",
        yaxis_title="Precipitation (inches)",
        legend_title="Legend",
        legend = dict(
            font= dict(size=15)
        ),
        template="plotly_white"
    )
    return fig