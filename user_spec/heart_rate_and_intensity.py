import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def plot_health_metrics(conn, user_id, start_date, end_date):
    """
    Creates a figure with two line plots showing average heart rate and average total intensity
    for a user within a specified date range, aggregated by day.
    
    Parameters:
    -----------
    conn : database connection
        Connection to the database containing user health data
    user_id : str or int
        The ID of the user whose data to plot
    start_date : str or datetime
        The start date for the data range (inclusive)
    end_date : str or datetime
        The end date for the data range (inclusive)
    
    Returns:
    --------
    plotly.graph_objects.Figure or None
        A plotly figure if data is available, None if no data is found
    """
    # Handle date format conversion
    if isinstance(start_date, datetime):
        start_date_str = start_date.strftime('%m/%d/%Y %H:%M:%S')
    else:
        try:
            temp_date = pd.to_datetime(start_date)
            start_date_str = temp_date.strftime('%m/%d/%Y %H:%M:%S')
        except:
            start_date_str = start_date
            
    if isinstance(end_date, datetime):
        end_date_str = end_date.strftime('%m/%d/%Y %H:%M:%S')
    else:
        try:
            temp_date = pd.to_datetime(end_date)
            end_date_str = temp_date.strftime('%m/%d/%Y %H:%M:%S')
        except:
            end_date_str = end_date
    
    # Query heart rate data for the specified user
    heart_rate_query = f"""
    SELECT Time, Value 
    FROM heart_rate 
    WHERE Id = '{user_id}'
    """
    
    # Query intensity data for the specified user
    intensity_query = f"""
    SELECT ActivityHour, TotalIntensity 
    FROM hourly_intensity 
    WHERE Id = '{user_id}'
    """
    
    # Execute queries to get all data for the user, then filter in Python
    try:
        heart_rate_df = pd.read_sql(heart_rate_query, conn)
        intensity_df = pd.read_sql(intensity_query, conn)
        
        # Convert time columns to datetime
        heart_rate_df['Time'] = pd.to_datetime(heart_rate_df['Time'], errors='coerce')
        intensity_df['ActivityHour'] = pd.to_datetime(intensity_df['ActivityHour'], errors='coerce')
        
        # Filter by date range in Python instead of SQL
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        heart_rate_df = heart_rate_df[(heart_rate_df['Time'] >= start_dt) & (heart_rate_df['Time'] <= end_dt)]
        intensity_df = intensity_df[(intensity_df['ActivityHour'] >= start_dt) & (intensity_df['ActivityHour'] <= end_dt)]
        
    except Exception as e:
        # Just return None instead of error message
        return None
    
    # Check if we have data
    if heart_rate_df.empty or intensity_df.empty:
        return None
    
    # Create day columns for heart rate data and intensity data
    heart_rate_df['Date'] = heart_rate_df['Time'].dt.date
    intensity_df['Date'] = intensity_df['ActivityHour'].dt.date
    
    # Group by date to get daily averages
    heart_rate_avg = heart_rate_df.groupby('Date')['Value'].mean().reset_index()
    intensity_avg = intensity_df.groupby('Date')['TotalIntensity'].sum().reset_index()  # Using sum for total intensity
    
    # Find common dates where both heart rate and intensity data exist
    common_dates = set(heart_rate_avg['Date']).intersection(set(intensity_avg['Date']))
    
    if not common_dates:
        return None
    
    # Filter to only include common dates
    heart_rate_avg = heart_rate_avg[heart_rate_avg['Date'].isin(common_dates)]
    intensity_avg = intensity_avg[intensity_avg['Date'].isin(common_dates)]
    
    # Sort by date
    heart_rate_avg = heart_rate_avg.sort_values('Date')
    intensity_avg = intensity_avg.sort_values('Date')
    
    # Create a figure
    fig = go.Figure()
    
    # Add heart rate trace with updated styling
    fig.add_trace(
        go.Scatter(
            x=heart_rate_avg['Date'],
            y=heart_rate_avg['Value'],
            mode='lines+markers',
            name="Average Heart Rate",
            line=dict(color='steelblue', width=4),
            marker=dict(symbol='circle', size=8)
        )
    )
    
    # Add intensity trace with updated styling
    fig.add_trace(
        go.Scatter(
            x=intensity_avg['Date'],
            y=intensity_avg['TotalIntensity'],
            mode='lines+markers',
            name="Total Intensity",
            line=dict(color='slategray', width=4),
            marker=dict(symbol='circle', size=8)
        )
    )
    
    # Update layout with new styling
    fig.update_layout(
        title="Daily Heart Rate and Physical Activity Intensity Trends",
        title_x=0.5,  # Centers the title
        xaxis_title='Date',
        yaxis_title='Average Heart Rate / Total Intensity',
        xaxis=dict(
            tickformat='%m/%d',
        ),
        legend=dict(
            title="Metrics",
            x=1.02,
            y=1,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.7)',
            font=dict(size=12),
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        ),
        template="plotly_white",
        height=400,
        width=800,
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=False
    )
    
    return fig