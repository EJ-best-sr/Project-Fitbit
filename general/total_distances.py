import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import pandas as pd


def plot_distances(df):
    total_distance_per_user = df.groupby('Id')['TotalDistance'].sum().reset_index()
    total_distance_per_user['Id'] = total_distance_per_user['Id'].astype(str)

    fig = px.bar(
        total_distance_per_user,
        x='Id',
        y='TotalDistance',
        labels={'Id': 'Users', 'TotalDistance': 'Total Distance'},
        width=800,  
        height=400
    )

    fig.update_traces(marker_color='steelblue')
    
    fig.update_layout(
        xaxis_title='Users', 
        yaxis_title='Total Distance',
        showlegend=False,
        template='plotly_white',
        xaxis_showticklabels=False,
        width=800,  
        height=400, 
        margin=dict(l=0, r=40, t=0, b=0),
        autosize=False, 
    )
    
    return fig

