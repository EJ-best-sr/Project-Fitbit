# # import plotly.graph_objects as go
# # import plotly.express as px
# # import statsmodels.api as sm
# # import scipy.stats as stats

# # def perform_regression_analysis(df_merged):
# #     """
# #     Perform regression analysis on the merged DataFrame and return Plotly figures.

# #     Args:
# #         df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.

# #     Returns:
# #         tuple: A tuple containing three Plotly figures:
# #             - Regression plot
# #             - Histogram of residuals
# #             - Q-Q plot of residuals
# #     """
# #     # Remove the sleep of less than 3 hours
# #     df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

# #     X = df_merged_filtered['TotalSedentaryMinutes']  # Independent variable
# #     y = df_merged_filtered['TotalSleepDuration']  # Dependent variable

# #     # Add a constant to the independent variable
# #     X = sm.add_constant(X)

# #     # Fit the OLS model
# #     model = sm.OLS(y, X).fit()
# #     print(model.summary())

# #     # Calculate predicted values and residuals
# #     predicted = model.predict(X)
# #     residuals = model.resid

# #     # Create the regression plot
# #     regression_fig = go.Figure()

# #     # Add scatter plot for the data points
# #     regression_fig.add_trace(
# #         go.Scatter(
# #             x=df_merged_filtered['TotalSedentaryMinutes'],
# #             y=df_merged_filtered['TotalSleepDuration'],
# #             mode='markers',
# #             #marker=dict(color='rgba(74, 55, 111, 0.8)'),  # Custom marker color
# #             name='Data Points'
# #         )
# #     )

# #     # Add regression line
# #     regression_fig.add_trace(
# #         go.Scatter(
# #             x=df_merged_filtered['TotalSedentaryMinutes'],
# #             y=predicted,
# #             mode='lines',
# #             line=dict(color='rgba(0, 0, 0)'),  # Custom line color
# #             name='Regression Line'
# #         )
# #     )

# #     # Update layout for the regression plot
# #     regression_fig.update_layout(
# #         title='Regression: Sedentary Time vs Sleep Time',
# #         xaxis_title='Total Sedentary Minutes',
# #         yaxis_title='Total Sleep Duration',
# #         showlegend=True,
# #         template='plotly_white',
# #         width=800,  
# #         height=400, 
# #         margin=dict(l=0, r=0, t=50, b=0),
# #         autosize=False, 
# #         legend=dict(
# #             x=0.02,  
# #             y=0.98, 
# #             xanchor='left',
# #             yanchor='top', 
# #             bgcolor='rgba(255, 255, 255, 0.5)',
# #             bordercolor='rgba(0, 0, 0, 0.5)',
# #             borderwidth=1 
# #         )
# #     )

# #     # Create the histogram of residuals
# #     residuals_histogram = px.histogram(
# #         x=residuals,
# #         nbins=30,
# #         labels={'x': 'Residuals', 'y': 'Frequency'},
# #         title='Histogram of Residuals',
# #         color_discrete_sequence=['rgba(69, 86, 128, 0.8)']  # Custom color
# #     )

# #     # Update layout for the histogram
# #     residuals_histogram.update_layout(
# #         template='plotly_white',
# #         width=800,  
# #         height=400, 
# #         margin=dict(l=0, r=0, t=50, b=0),
# #         autosize=False, 
# #     )

# #     # Create the Q-Q plot
# #     qq_fig = go.Figure()

# #     (theoretical_quantiles, sample_quantiles), (slope, intercept, _) = stats.probplot(residuals, dist="norm")    
# #     # Add scatter plot for the Q-Q points
# #     qq_fig.add_trace(
# #         go.Scatter(
# #             x=theoretical_quantiles,
# #             y=sample_quantiles,
# #             mode='markers',
# #             marker=dict(color='rgba(69, 86, 128, 0.8)', line=dict(color='black', width=1)),
# #             name='Q-Q Points'
# #         )
# #     )


# #     qq_fig.add_trace(
# #         go.Scatter(
# #             x=[theoretical_quantiles.min(), theoretical_quantiles.max()],
# #             y=[theoretical_quantiles.min(), theoretical_quantiles.max()],
# #             mode='lines',
# #             line=dict(color='rgba(44, 131, 127, 1)', dash='dash'),
# #             name='Theoretical Line'
# #         )
# #     )

# #     # Update layout for the Q-Q plot
# #     qq_fig.update_layout(
# #         title='Q-Q Plot of Residuals',
# #         xaxis_title='Theoretical Quantiles of Normal Distribution',
# #         yaxis_title='Sample Quantiles',
# #         showlegend=True,
# #         template='plotly_white',
# #         width=800,  
# #         height=400,
# #         autosize=False, 
# #         margin=dict(l=0, r=0, t=50, b=0),
# #         legend=dict(
# #             x=0.02,  
# #             y=0.98, 
# #             xanchor='left',
# #             yanchor='top', 
# #             bgcolor='rgba(255, 255, 255, 0.5)',
# #             bordercolor='rgba(0, 0, 0, 0.5)',
# #             borderwidth=1 
# #         ) 
# #     )

# #     return regression_fig, residuals_histogram, qq_fig


# import plotly.graph_objects as go
# import plotly.express as px
# import statsmodels.api as sm
# import scipy.stats as stats
# import numpy as np

# def perform_regression_analysis(df_merged):
#     """
#     Perform regression analysis on the merged DataFrame and return Plotly figures.

#     Args:
#         df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.

#     Returns:
#         tuple: A tuple containing three Plotly figures:
#             - Regression plot
#             - Histogram of residuals
#             - Q-Q plot of residuals
#     """
#     # Remove the sleep of less than 3 hours
#     df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

#     X = df_merged_filtered['TotalSedentaryMinutes']  # Independent variable
#     y = df_merged_filtered['TotalSleepDuration']  # Dependent variable

#     # Add a constant to the independent variable
#     X = sm.add_constant(X)

#     # Fit the OLS model
#     model = sm.OLS(y, X).fit()
#     print(model.summary())

#     # Calculate predicted values and residuals
#     predicted = model.predict(X)
#     residuals = model.resid

#     # Create the regression plot
#     regression_fig = go.Figure()

#     # Add scatter plot for the data points
#     regression_fig.add_trace(
#         go.Scatter(
#             x=df_merged_filtered['TotalSedentaryMinutes'],
#             y=df_merged_filtered['TotalSleepDuration'],
#             mode='markers',
#             name='Data Points'
#         )
#     )

#     # Add regression line
#     regression_fig.add_trace(
#         go.Scatter(
#             x=df_merged_filtered['TotalSedentaryMinutes'],
#             y=predicted,
#             mode='lines',
#             line=dict(color='rgba(0, 0, 0)'),  # Custom line color
#             name='Regression Line'
#         )
#     )

#     # Update layout for the regression plot
#     regression_fig.update_layout(
#         title='Regression: Sedentary Time vs Sleep Time',
#         xaxis_title='Total Sedentary Minutes',
#         yaxis_title='Total Sleep Duration',
#         showlegend=True,
#         template='plotly_white',
#         width=800,  
#         height=400, 
#         margin=dict(l=0, r=0, t=50, b=0),
#         autosize=False, 
#         legend=dict(
#             x=0.02,  
#             y=0.98, 
#             xanchor='left',
#             yanchor='top', 
#             bgcolor='rgba(255, 255, 255, 0.5)',
#             bordercolor='rgba(0, 0, 0, 0.5)',
#             borderwidth=1 
#         )
#     )

#     # Create the histogram of residuals with KDE
#     residuals_histogram = px.histogram(
#         x=residuals,
#         nbins=30,
#         labels={'x': 'Residuals', 'y': 'Frequency'},
#         title='Histogram of Residuals',
#         color_discrete_sequence=['rgba(69, 86, 128, 0.8)'],  # Custom color
#         marginal='rug',  # Add rug plot
#     )

#     # Add KDE line to the histogram
#     kde_x = np.linspace(residuals.min(), residuals.max(), 1000)
#     kde_y = stats.gaussian_kde(residuals)(kde_x)
#     residuals_histogram.add_trace(
#         go.Scatter(
#             x=kde_x,
#             y=kde_y * len(residuals) * (residuals.max() - residuals.min()) / 30,  # Scale KDE to match histogram
#             mode='lines',
#             line=dict(color='rgba(255, 0, 0, 0.8)'),  # Red KDE line
#             name='KDE'
#         )
#     )

#     # Update layout for the histogram
#     residuals_histogram.update_layout(
#         template='plotly_white',
#         width=800,  
#         height=400, 
#         margin=dict(l=0, r=0, t=50, b=0),
#         autosize=False, 
#     )

#     # Create the Q-Q plot
#     qq_fig = go.Figure()

#     # Calculate theoretical and sample quantiles
#     (theoretical_quantiles, sample_quantiles), (slope, intercept, _) = stats.probplot(residuals, dist="norm")

#     # Add scatter plot for the Q-Q points
#     qq_fig.add_trace(
#         go.Scatter(
#             x=theoretical_quantiles,
#             y=sample_quantiles,
#             mode='markers',
#             marker=dict(color='rgba(69, 86, 128, 0.8)', line=dict(color='black', width=1)),
#             name='Q-Q Points'
#         )
#     )

#     # Add theoretical line (y = x)
#     qq_fig.add_trace(
#         go.Scatter(
#             x=[theoretical_quantiles.min(), theoretical_quantiles.max()],
#             y=[theoretical_quantiles.min(), theoretical_quantiles.max()],
#             mode='lines',
#             line=dict(color='rgba(44, 131, 127, 1)', dash='dash'),
#             name='Theoretical Line'
#         )
#     )

#     # Update layout for the Q-Q plot
#     qq_fig.update_layout(
#         title='Q-Q Plot of Residuals',
#         xaxis_title='Theoretical Quantiles of Normal Distribution',
#         yaxis_title='Sample Quantiles',
#         showlegend=True,
#         template='plotly_white',
#         width=800,  
#         height=400,
#         autosize=False, 
#         margin=dict(l=0, r=0, t=50, b=0),
#         legend=dict(
#             x=0.02,  
#             y=0.98, 
#             xanchor='left',
#             yanchor='top', 
#             bgcolor='rgba(255, 255, 255, 0.5)',
#             bordercolor='rgba(0, 0, 0, 0.5)',
#             borderwidth=1 
#         ) 
#     )

#     return regression_fig, residuals_histogram, qq_fig


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

    # Add a constant to the independent variable
    X = sm.add_constant(X)

    # Fit the OLS model
    model = sm.OLS(y, X).fit()
    print(model.summary())

    # Calculate predicted values and residuals
    predicted = model.predict(X)
    residuals = model.resid

    regression_fig = go.Figure()
    regression_fig.add_trace(
        go.Scatter(
            x=df_merged_filtered['TotalSedentaryMinutes'],
            y=df_merged_filtered['TotalSleepDuration'],
            mode='markers',
            name='Data Points',
            marker=dict(color='rgba(69, 86, 128, 0.8)', line=dict(color='rgba(69, 86, 128, 0.8)', width=1)),

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
            x=0.02,  
            y=0.98, 
            xanchor='left',
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
        color_discrete_sequence=['rgba(69, 86, 128, 0.8)'], 
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
            marker=dict(color='rgba(69, 86, 128, 0.8)', line=dict(color='rgba(69, 86, 128, 0.8)', width=1)),
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

    return regression_fig, residuals_histogram, qq_fig