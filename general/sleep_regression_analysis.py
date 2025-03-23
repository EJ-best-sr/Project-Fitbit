import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
import scipy.stats as stats
import numpy as np

def perform_regression_analysis(df_merged):
    """
    Perform regression analysis on the merged DataFrame and return Plotly figures.

    Args:
        df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.

    Returns:
        tuple: A tuple containing three Plotly figures:
            - Regression plot
            - Histogram of residuals (density-scaled)
            - Q-Q plot of residuals with correct fitted line
    """
    # Remove the sleep of less than 3 hours
    df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

    X = df_merged_filtered['TotalSedentaryMinutes']  # Independent variable
    y = df_merged_filtered['TotalSleepDuration']  # Dependent variable
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    predicted = model.predict(X)
    residuals = model.resid

    regression_fig = go.Figure()
    regression_fig.add_trace(
        go.Scatter(
            x=df_merged_filtered['TotalSedentaryMinutes'],
            y=df_merged_filtered['TotalSleepDuration'],
            mode='markers',
            name='Data Points',
            marker=dict(color='steelblue', line=dict(color='steelblue', width=1)),

        )
    )

    # regression line
    regression_fig.add_trace(
        go.Scatter(
            x=df_merged_filtered['TotalSedentaryMinutes'],
            y=predicted,
            mode='lines',
            line=dict(color='rgba(0, 0, 0)'),
            name='Regression Line'
        )
    )

    regression_fig.update_layout(
        title='Regression: Sedentary Time vs Sleep Time',
        xaxis_title='Total Sedentary Minutes',
        yaxis_title='Total Sleep Duration',
        showlegend=True,
        template='plotly_white',
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

    # Create the histogram of residuals (density-scaled)
    residuals_histogram = px.histogram(
        x=residuals,
        nbins=30,
        labels={'x': 'Residuals', 'y': 'Density'},
        title='Histogram of Residuals (Density-Scaled)',
        color_discrete_sequence=['rgba(70, 130, 180, 0.7)'], 
        histnorm='density',
        marginal='rug', 
    )

    kde_x = np.linspace(residuals.min(), residuals.max(), 1000)
    kde_y = stats.gaussian_kde(residuals)(kde_x)
    bin_width = (residuals.max() - residuals.min()) / 5 
    kde_y = kde_y * bin_width

    residuals_histogram.add_trace(
        go.Scatter(
            x=kde_x,
            y=kde_y,
            mode='lines',
            line=dict(color='rgba(0, 0, 0)'),
            name='KDE'
        )
    )

    residuals_histogram.update_traces(
    marker=dict(
        line=dict(
            color='rgba(70, 130, 180, 0.9)',  # Black border for bins
            width=1  # Border width
        )
    )
)

    residuals_histogram.update_layout(
        template='plotly_white',
        width=800,  
        height=400, 
        margin=dict(l=0, r=0, t=50, b=0),
        autosize=False, 
    )

    qq_fig = go.Figure()

    (theoretical_quantiles, sample_quantiles), (slope, intercept, _) = stats.probplot(residuals, dist="norm")
    qq_fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=sample_quantiles,
            mode='markers',
            marker=dict(color='steelblue', line=dict(color='steelblue', width=1)),
            name='Q-Q Points'
        )
    )

    qq_fig.add_trace(
        go.Scatter(
            x=[theoretical_quantiles.min(), theoretical_quantiles.max()],
            y=[slope * theoretical_quantiles.min() + intercept, slope * theoretical_quantiles.max() + intercept],
            mode='lines',
            line=dict(color='rgba(0, 0, 0)'),
            name='Theoretical Line'
        )
    )

    qq_fig.update_layout(
        title='Q-Q Plot of Residuals',
        xaxis_title='Theoretical Quantiles of Normal Distribution',
        yaxis_title='Sample Quantiles',
        showlegend=True,
        template='plotly_white',
        width=800,  
        height=400,
        autosize=False, 
        margin=dict(l=0, r=0, t=50, b=0),
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

    p_value = model.pvalues['TotalSedentaryMinutes'] 
    alpha = 0.05
    if p_value < alpha:
        msg = "There is some statistically significant relationship between TotalSedentaryMinutes and TotalSleepDuration"
    else:
        msg = "There is NO statistically significant relationship between TotalSedentaryMinutes and TotalSleepDuration"
    info = f"R-squared value is {model.rsquared:.4f} and p-value is {p_value:.4f}. **The model explains {model.rsquared*100:.2f}% of the variation** in TotalSleepDuration based on TotalSedentaryMinutes. {msg} (significance level is {alpha})."


    return regression_fig, residuals_histogram, qq_fig, info