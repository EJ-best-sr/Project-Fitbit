import sqlite3
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go

def calories_vs_steps_regression(db_path):
    conn = sqlite3.connect(db_path)

    query_steps = '''
    SELECT Id,
        ActivityDate, 
        TotalSteps,
        Calories
    FROM daily_activity
    '''
    df_steps = pd.read_sql_query(query_steps, conn)
    df_steps['ActivityDate'] = pd.to_datetime(df_steps['ActivityDate']).dt.date

    X = df_steps['TotalSteps']  # Independent variable (total active minutes on day 1)
    y = df_steps['Calories']  # Dependent variable (total sleep duration from evening of day 1 to morning of day 2)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    predicted = model.predict(X)

    regression_fig = go.Figure()

    # Add scatter plot for the data points
    regression_fig.add_trace(
        go.Scatter(
            x = df_steps['TotalSteps'],
            y = df_steps['Calories'],
            mode='markers',
            name ='Data Points',
            marker=dict(color='steelblue', line=dict(color='steelblue', width=1)),
        )
    )

    regression_fig.add_trace(
        go.Scatter(
            x = df_steps['TotalSteps'],
            y=predicted,
            mode='lines',
            line=dict(color='rgba(0, 0, 0)'),  
            name='Regression Line'
        )
    )

    regression_fig.update_layout(
        xaxis_title='Calories Burned',
        yaxis_title='Steps',
        showlegend=True,
        template='plotly_white',
        width=800,  
        height=400,
        autosize=False, 
        margin=dict(l=100, r=100, t=50, b=0),
        legend=dict(
            x=0.02,  
            y=0.98, 
            xanchor='left',
            yanchor='top', 
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1 
        )
    )

    conn.close()

    p_value = model.pvalues['TotalSteps'] 
    alpha = 0.05
    if p_value < alpha:
        msg = "There is a statistically significant relationship between TotalSteps and Calories"
    else:
        msg = "There is NO statistically significant relationship between TotalSteps and Calories"
    info = f"R-squared value is {model.rsquared:.4f} and p-value is {p_value:.2e}. **The model explains {model.rsquared*100:.2f}% of the variation** in Calories (Burned) based on TotalSteps. {msg} (significance level is {alpha})."

    
    return regression_fig, info