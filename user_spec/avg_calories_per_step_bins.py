import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def avg_calories_per_step_bins(db_path):
    """
    Creates interactive bar and box plots for average calories burned by steps bins.
    
    Args:
        db_path (str): Path to the SQLite database.
        
    Returns:
        tuple: A tuple containing the bar plot figure and the box plot figure.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Query to fetch data
    query_steps = '''
    SELECT Id, 
           TotalSteps,
           Calories
    FROM daily_activity
    '''
    df = pd.read_sql_query(query_steps, conn)

    # Bin the TotalSteps into categories
    df['StepsBins'] = pd.cut(
        df['TotalSteps'],
        bins=[0, 1000, 2000, 5000, 7000, 10000, 15000, float('inf')],
        labels=['0-1k', '1-2k', '2-5k', '5k-7k', '7k-10k', '10k-15k', '15k+']
    )

    # Group by StepsBins and calculate mean Calories
    df_grouped = df.groupby('StepsBins')['Calories'].mean().reset_index()

    # Bar plot with Plotly
    fig_bar = px.bar(
        df_grouped,
        x='StepsBins',
        y='Calories',
        title='Bar Plot: Average Calories Burned by Total Steps Bins',
        labels={'StepsBins': 'Total Steps In a Day', 'Calories': 'Average Calories Burned'},
        text='Calories',  # Add text labels on bars
        color='StepsBins',  # Color bars by StepsBins
        color_discrete_sequence=px.colors.sequential.Viridis  # Use Viridis color scale
    )

    # Add a trend line to the bar plot
    fig_bar.add_trace(
        go.Scatter(
            x=df_grouped['StepsBins'],
            y=df_grouped['Calories'],
            mode='lines+markers',
            name='Trend Line',
            line=dict(color='black', width=2),
            marker=dict(color='black', size=8)
        )
    )

    fig_bar.update_layout(
        showlegend=True,
        xaxis_title='Total Steps In a Day',
        yaxis_title='Average Calories Burned',
        template='plotly_white'  
    )

    fig_box = px.box(
        df,
        x='StepsBins',
        y='Calories',
        title='Box Plot: Calories Burned by Total Steps Bins',
        labels={'StepsBins': 'Total Steps Bins', 'Calories': 'Calories Burned'},
    )

    fig_box.update_layout(
        xaxis_title='Total Steps Bins',
        yaxis_title='Calories Burned',
        template='plotly_white' 
    )

    return fig_bar, fig_box