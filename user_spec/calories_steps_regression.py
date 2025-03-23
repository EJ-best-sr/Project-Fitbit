import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import numpy as np

def plot_regression_line(df, user_id):
    """
    Returns a Plotly figure showing a regression line for Total Steps vs Calories Burnt.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        user_id (int): The ID of the user to filter the data.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object.
    """
    # Filter data for the specific user
    user_data = df[df['Id'] == user_id]
    
    # Check if the filtered data is empty
    if user_data.empty:
        raise ValueError(f"No data found for User {user_id}.")
    
    # Calculate the regression line using Seaborn (for simplicity)
    slope, intercept = np.polyfit(user_data['TotalSteps'], user_data['Calories'], 1)
    regression_line = slope * user_data['TotalSteps'] + intercept
    
    # Create a scatter plot with Plotly
    fig = go.Figure()
    
    # Add scatter plot for the data points
    fig.add_trace(
        go.Scatter(
            x=user_data['TotalSteps'],
            y=user_data['Calories'],
            mode='markers',
            marker=dict(color='steelblue', size=8),
            name='Data Points'
        )
    )
    
    # Add regression line
    fig.add_trace(
        go.Scatter(
            x=user_data['TotalSteps'],
            y=regression_line,
            mode='lines',
            line=dict(color='black'), 
            name='Regression Line'
        )
    )
    
    fig.update_layout(
        xaxis_title='Total Steps',
        yaxis_title='Calories',
        showlegend=True,
        template='plotly_white',
        width=800,  
        height=400, 
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=False, 
        legend=dict(
            x=0.02,  
            y=0.98, 
            xanchor='left',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )
    
    return fig