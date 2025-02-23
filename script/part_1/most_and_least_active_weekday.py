import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_weekday_activity(df):
    df['Weekday'] = pd.to_datetime(df['ActivityDate']).dt.day_name()
    weekly_data = df[['Id', 'ActivityDate', 'TotalSteps', 'Weekday']]
    numeric_columns = weekly_data.select_dtypes(include='number')
    sortByDays = numeric_columns.groupby(weekly_data['Weekday']).sum()
    plot_df = sortByDays.reset_index()
    plt.figure(figsize = (10,8))
    sns.barplot(data = plot_df, x = 'TotalSteps', y = 'Weekday', palette = 'viridis', hue = 'Weekday' , legend = None)
    plt.title("Weekday activity")
    plt.show()