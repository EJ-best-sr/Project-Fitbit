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
            line=dict(color='rgba(0, 0, 0)'),  # Custom line color
            name='Regression Line'
        )
    )

    conn.close()
    
    return regression_fig

