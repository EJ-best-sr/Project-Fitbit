import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_workout_frequency_by_day(df):
    """
    Plots the frequency of workouts by day of the week.

    Parameters:
    df (pd.DataFrame): The dataset containing 'ActivityDate'.
    """
    # Extract day of the week from ActivityDate
    df['DayOfWeek'] = pd.to_datetime(df['ActivityDate']).dt.day_name()

    # Count workouts per day
    workout_frequency = df['DayOfWeek'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])

    # Plot the results
    plt.figure(figsize=(10, 6))
    sns.barplot(x=workout_frequency.index, y=workout_frequency.values, hue=workout_frequency.index, palette='viridis', legend=False)
    plt.title('Workout Frequency by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Frequency')
    plt.show()
    