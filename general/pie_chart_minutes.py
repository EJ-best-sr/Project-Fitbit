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

    labels = ["Lightly Active", "Very Active", "Fairly Active"]
    colors = ["#c5e6fc", "#1f77b4", "#78b4de"]

    if sum(active_minutes) == 0:
        st.warning("No activity data found.")
        return None

    font_sizes = [20 if label == "Lightly Active" else 14 for label in labels]

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
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=False, 
        legend=dict(
            x=0.98,  
            y=0.70, 
            xanchor='right',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )

    return fig
