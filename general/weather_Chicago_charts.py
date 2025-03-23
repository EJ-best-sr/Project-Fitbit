import pandas as pd
import plotly.graph_objects as go

def plot_precipitation_chart(data: pd.DataFrame):
    """
    Plot daily precipitation as bars and cumulative precipitation as an area chart.

    Parameters:
    - data (pd.DataFrame):  'datetime' and 'precip' columns.
    """
    df = data.copy()

    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")

    df["precip"] = df["precip"].fillna(0)
    df["precip_cumulative"] = df["precip"].cumsum()

    fig = go.Figure()

    # Bar chart: daily precipitation
    fig.add_trace(go.Bar(
        x=df["datetime"],
        y=df["precip"],
        name="Precipitation",
        marker_color="rgba(70, 130, 180, 0.8)"
    ))

    # Area chart: cumulative precipitation
    fig.add_trace(go.Scatter(
    x=df["datetime"],
    y=df["precip_cumulative"],
    name="Cumulative",
    mode="lines",
    fill="tozeroy",
    line=dict(color="rgba(70, 130, 180, 0.7)", width=3),
    fillcolor="rgba(70, 130, 180, 0.2)"  # same color, lighter fill
    ))

    # Layout styling
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Precipitation (inches)",
        legend_title="Legend",
        legend = dict(
            font= dict(size=15),
            bgcolor="rgba(255,255,255,0.7)", 
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1),
        template="plotly_white",
        width=800,               
        height=550,  
    )
    return fig