import pandas as pd
import plotly.graph_objects as go

def plot_steps_and_distance(data, selected_user, start_date, end_date):
    """
    Plots total steps as bars and total distance as a line per day for a given user within a specified date range.

    Parameters:
        data (DataFrame): The DataFrame containing user activity data.
        selected_user (int): The ID of the user.
        start_date (str): The start date in the format 'MM/DD/YYYY'.
        end_date (str): The end date in the format 'MM/DD/YYYY'.

    Returns:
        plotly.graph_objs._figure.Figure: An interactive plot with total steps as bars and total distance as a line per day.
    """
    # Filter the data based on the selected user and the date range
    filtered_data = data[
        (data['Id'] == selected_user) & 
        (data['ActivityDate'] >= start_date) & 
        (data['ActivityDate'] <= end_date)
    ].copy()
    
    # Convert 'ActivityDate' to datetime format
    filtered_data['ActivityDate'] = pd.to_datetime(filtered_data['ActivityDate'])
    
    # Convert distance to meters
    filtered_data['TotalDistanceMeters'] = filtered_data['TotalDistance'] * 1000  # kilometers to meters
    
    # Create the figure
    fig = go.Figure()

    # Add the bar plot for total steps
    fig.add_trace(go.Bar(
        x=filtered_data['ActivityDate'],
        y=filtered_data['TotalSteps'],
        name='Total Steps',
    ))

    # Add the line plot for total distance
    fig.add_trace(go.Scatter(
        x=filtered_data['ActivityDate'],
        y=filtered_data['TotalDistanceMeters'],
        name='Total Distance (m)',
        mode='lines+markers',
        marker=dict(symbol='circle')
    ))


    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Steps / Distance (m)',
        barmode='group',
        legend_title="Metrics",
        margin=dict(l=0, r=0, t=0, b=0), # update here the margins (especially the top one!)
        legend=dict( # legend inside of the plot
            x=0.98,  
            y=0.92, 
            xanchor='right',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=0.5
        )
    )
    
    return fig

