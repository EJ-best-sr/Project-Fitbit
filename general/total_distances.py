import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import pandas as pd


def plot_distances(df):
    # Aggregate total distance per user
    total_distance_per_user = df.groupby('Id')['TotalDistance'].sum().reset_index()
    # Convert Id to string (categorical)
    total_distance_per_user['Id'] = total_distance_per_user['Id'].astype(str)

    # Create an interactive bar plot using Plotly
    fig = px.bar(
        total_distance_per_user,
        x='Id',
        y='TotalDistance',
        labels={'Id': 'Users', 'TotalDistance': 'Total Distance'},
        width=600,  # Increase the width
        height=400
    )
    
    # Customize the layout (optional)
    fig.update_layout(
        xaxis_title='', 
        yaxis_title='Total Distance',
        showlegend=False,
        template='plotly_white',
        xaxis_showticklabels=False 
    )
    
    return fig

