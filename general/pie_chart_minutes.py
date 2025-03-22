import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def plot_activity_distribution(user_data):
    active_minutes = [
        user_data['LightlyActiveMinutes'].sum(),
        user_data['VeryActiveMinutes'].sum(),
        user_data['FairlyActiveMinutes'].sum()
    ]

    active_minutes = [round(value, 1) for value in active_minutes]

    labels = ["Lightly Active", "Fairly Active", "Very Active"]
    colors = ['lightblue', "steelblue",  "slategray"]

    if sum(active_minutes) == 0:
        st.warning("No activity data found.")
        return None

    font_sizes = [40 if label == "Lightly Active" else 16 for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=active_minutes, 
        hoverinfo="label+percent", 
        textinfo="percent", 
        insidetextorientation="horizontal",  
        textfont=dict(color="white", size=font_sizes), 
        marker=dict(colors=colors)
    )])

    fig.update_layout(
    showlegend=True,
    template='plotly_white',
    legend=dict(
        title="Activity Levels",
        font=dict(size=14),         
        bgcolor='rgba(240, 240, 240, 0.8)', 
        bordercolor='gray',          
        borderwidth=1,               
        x=1,                        
        y=0.5,                       
    )
)

    return fig