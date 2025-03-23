import sqlite3
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import scipy.stats as stats

def plot_bmi_relationship(db_path: str):
    conn = sqlite3.connect(db_path)
    daily = pd.read_sql_query("SELECT * FROM daily_activity", conn)
    weight = pd.read_sql_query("SELECT * FROM weight_log", conn)
    conn.close()

    daily['ActivityDate'] = pd.to_datetime(daily['ActivityDate'])
    weight['Date'] = pd.to_datetime(weight['Date']).dt.normalize()

    merged_df = pd.merge(
        daily,
        weight,
        how='inner',
        left_on=['Id', 'ActivityDate'],
        right_on=['Id', 'Date']
    )

    merged_df['TotalActiveMinutes'] = (
        merged_df['VeryActiveMinutes'] +
        merged_df['FairlyActiveMinutes'] +
        merged_df['LightlyActiveMinutes']
    )

    # --- Plot 1: Sedentary Minutes vs BMI ---
    x1 = merged_df['SedentaryMinutes'].values.reshape(-1, 1)
    y1 = merged_df['BMI'].values
    model1 = LinearRegression().fit(x1, y1)
    y1_pred = model1.predict(x1)

    r_squared_1 = model1.score(x1, y1)
    slope1, intercept1, r_val1, p_val1, std_err1 = stats.linregress(merged_df['SedentaryMinutes'], merged_df['BMI'])

    text1 = (f"R-squared value is {r_squared_1:.4f} and p-value is {p_val1:.2e}. "
             f"**The model explains {r_squared_1 * 100:.2f}% of the variation** in BMI based on Sedentary Minutes. "
             f"{'There is a statistically significant relationship' if p_val1 < 0.05 else 'There is no statistically significant relationship'} "
             f"(significance level is 0.05).")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=merged_df['SedentaryMinutes'],
        y=merged_df['BMI'],
        mode='markers',
        name='Data Points',
        marker=dict(color='steelblue', size=6, opacity=1)
    ))
    fig1.add_trace(go.Scatter(
        x=merged_df['SedentaryMinutes'],
        y=y1_pred,
        mode='lines',
        name='Regression Line',
        line=dict(color='black', width=2)
    ))
   
    fig1.update_layout(
        xaxis_title='Sedentary Minutes', 
        yaxis_title='BMI',
        width=800,  
        height=400, 
        margin=dict(l=0, r=0, t=50, b=0),
        autosize=False, 
        legend=dict(
            x=0.98,  
            y=0.98, 
            xanchor='right',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )

    # --- Plot 2: Total Active Minutes vs BMI ---
    x2 = merged_df['TotalActiveMinutes'].values.reshape(-1, 1)
    y2 = merged_df['BMI'].values
    model2 = LinearRegression().fit(x2, y2)
    y2_pred = model2.predict(x2)

    r_squared_2 = model2.score(x2, y2)
    slope2, intercept2, r_val2, p_val2, std_err2 = stats.linregress(merged_df['TotalActiveMinutes'], merged_df['BMI'])

    text2 = (f"R-squared value is {r_squared_2:.4f} and p-value is {p_val2:.2e}. "
             f"**The model explains {r_squared_2 * 100:.2f}% of the variation** in BMI based on Total Active Minutes. "
             f"{'There is a statistically significant relationship' if p_val2 < 0.05 else 'There is no statistically significant relationship'} "
             f"(significance level is 0.05).")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=merged_df['TotalActiveMinutes'],
        y=merged_df['BMI'],
        mode='markers',
        name='Data Points',
        marker=dict(color='steelblue', size=6, opacity=1)
    ))
    fig2.add_trace(go.Scatter(
        x=merged_df['TotalActiveMinutes'],
        y=y2_pred,
        mode='lines',
        name='Regression Line',
        line=dict(color='black', width=2)
    ))
   
    fig2.update_layout(
        xaxis_title='Total Active Minutes', 
        yaxis_title='BMI',
        width=800,  
        height=400, 
        margin=dict(l=0, r=0, t=50, b=0),
        autosize=False, 
        legend=dict(
            x=0.98,  
            y=0.98, 
            xanchor='right',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )

    return fig1, fig2, text1, text2