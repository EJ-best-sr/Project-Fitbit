import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
def plot_bmi_distribution(db_path):
    """
    Fetches BMI data from the Fitbit database and plots a histogram showing
    the distribution of BMI values using Plotly.
    
    Parameters:
    None
    
    Returns:
    - fig: A Plotly figure object containing the histogram.
    """
    connection = sqlite3.connect(db_path)
    
    # Query weight_log table to get BMI values
    query = "SELECT BMI FROM weight_log"
    weight_data = pd.read_sql_query(query, connection)
    
    # Close database connection
    connection.close()
    
    # Drop missing BMI values
    weight_data.dropna(inplace=True)

    # Create the histogram figure
    fig = px.histogram(
        weight_data,
        x="BMI",
        nbins=30,
        title="BMI Distribution of Fitbit Users",
        labels={"BMI": "BMI", "count": "Frequency"},
        color_discrete_sequence=['royalblue'],
        opacity=0.8,
    )

    # Compute the histogram counts manually using numpy.histogram
    counts, bins = np.histogram(weight_data["BMI"], bins=30)
    max_bin_count = counts.max()

    # Define BMI category reference lines
    bmi_categories = [
        {"value": 18.5, "color": "green",  "label": "Underweight (18.5)"},
        {"value": 24.9, "color": "blue",   "label": "Normal (18.5 - 24.9)"},
        {"value": 29.9, "color": "orange", "label": "Overweight (25 - 29.9)"},
        {"value": 30,   "color": "red",    "label": "Obese (30+)"},
    ]

    # Add reference lines that reach up to max_bin_count
    for cat in bmi_categories:
        fig.add_trace(
            go.Scatter(
                x=[cat["value"], cat["value"]],
                y=[0, max_bin_count],
                mode="lines",
                line=dict(color=cat["color"], dash="dash"),
                name=cat["label"],
            )
        )

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="BMI",
        yaxis_title="Frequency",
        showlegend=True,
        template="plotly_white",
        width=800,
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
    )

    return fig