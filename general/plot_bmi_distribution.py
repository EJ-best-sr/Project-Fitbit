import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_bmi_distribution(db_path):
    """
    Fetches BMI data from the Fitbit database and plots a histogram showing
    the distribution of BMI values using Plotly.
    
    Parameters:
    None
    
    Returns:
    - fig: A Plotly figure object containing the histogram.
    """
    # Connect to the database
    connection = sqlite3.connect(db_path)
    
    # Query weight_log table to get BMI values
    query = "SELECT BMI FROM weight_log"
    weight_data = pd.read_sql_query(query, connection)
    
    # Close database connection
    connection.close()
    
    # Drop missing BMI values
    weight_data.dropna(inplace=True)
    
    # Create BMI Distribution Histogram using Plotly
    fig = px.histogram(
        weight_data,
        x="BMI",
        nbins=30,
        title="BMI Distribution of Fitbit Users",
        labels={"BMI": "BMI", "count": "Frequency"},
        color_discrete_sequence=['royalblue'],  # Set histogram color
        opacity=0.8,  # Adjust opacity
    )

    # Add BMI category reference lines
    bmi_categories = [
        {"value": 18.5, "color": "green", "label": "Underweight (18.5)"},
        {"value": 24.9, "color": "blue", "label": "Normal (18.5 - 24.9)"},
        {"value": 29.9, "color": "orange", "label": "Overweight (25 - 29.9)"},
        {"value": 30, "color": "red", "label": "Obese (30+)"},
    ]

    for category in bmi_categories:
        fig.add_trace(
            go.Scatter(
                x=[category["value"], category["value"]],
                y=[0, weight_data["BMI"].value_counts().max()],  # Span the full height of the histogram
                mode="lines",
                line=dict(color=category["color"], dash="dash"),
                name=category["label"],
            )
        )

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="BMI",
        yaxis_title="Frequency",
        showlegend=True,
        template="plotly_white",  # Use a clean template
        width=800,  # Set width of the plot
        height=500,  # Set height of the plot
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
    )

    return fig