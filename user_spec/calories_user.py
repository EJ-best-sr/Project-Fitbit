import plotly.express as px
import pandas as pd

def plot_calories_burnt(data, user_id, start_date, end_date):
    """
    Plots a bar chart of calories burnt for a specific user between a start and end date.

    Parameters:
        data (pd.DataFrame): DataFrame containing user activity data.
        user_id (int): The ID of the user to plot.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        fig (plotly.graph_objs._figure.Figure): Plotly bar chart figure.
    """
    # Filter the data for the given user and date range
    user_data = data[
        (data['Id'] == user_id) & 
        (data['ActivityDate'] >= start_date) & 
        (data['ActivityDate'] <= end_date)
    ]

    # Group by date and calculate total calories burnt per day
    daily_calories = user_data.groupby('ActivityDate')['Calories'].sum().reset_index()

    # Create the bar chart using Plotly
    fig = px.bar(
        daily_calories, 
        x='ActivityDate', 
        y='Calories', 
        labels={'Calories': 'Calories Burnt', 'ActivityDate': 'Date'}
    )

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Calories Burnt',
        bargap=0.2,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig
