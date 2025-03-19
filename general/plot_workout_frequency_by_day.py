import pandas as pd
import plotly.express as px

def plot_workout_frequency_by_day(df):
    """
    Returns a Plotly figure showing the frequency of workouts by day of the week.

    Parameters:
        df (pd.DataFrame): The dataset containing 'ActivityDate'.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object.
    """
    df['DayOfWeek'] = pd.to_datetime(df['ActivityDate']).dt.day_name()

    workout_frequency = df['DayOfWeek'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])


    fig = px.bar(
        x=workout_frequency.index,
        y=workout_frequency.values,
        labels={'x': 'Day of the Week', 'y': 'Frequency'},
        #rcolor=workout_frequency.index,
        #color_discrete_sequence=px.colors.sequential.Viridis 
    )

    fig.update_layout(
        showlegend=False,  # Hide legend
        xaxis_title='Day of the Week',
        yaxis_title='Frequency',
        template='plotly_white',
        width = 800,
        height = 400
    )

    return fig