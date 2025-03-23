import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def plot_activities(user_data):
    active_minutes = [
        user_data['LightlyActiveMinutes'].sum(),
        user_data['VeryActiveMinutes'].sum(),
        user_data['FairlyActiveMinutes'].sum()
    ]

    active_minutes = [round(value, 1) for value in active_minutes]

    labels = ["Lightly Active", "Fairly Active", "Very Active"]
    colors = [
        'rgba(173, 216, 230, 0.9)',  # light blue with 60% opacity
        'rgba(70, 130, 180, 0.7)',   # steelblue with 80% opacity
        'rgba(112, 128, 144, 0.8)'   # slategray with 100% opacity
]

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
        width=800,  
        height=400,  
        margin=dict(l=0, r=50, t=50, b=0), 
        legend=dict(
            title="Activity Levels",
            font=dict(size=14),         
            bgcolor='rgba(255, 255, 255, 0.5)',  
            bordercolor='black',          
            borderwidth=1,               
            x=0.80,                        
            y=0.80,                       
        ) 
    )

    return fig