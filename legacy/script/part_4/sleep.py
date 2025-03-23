import sqlite3
from traceback import print_tb
from matplotlib import use
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# get the dataframe that contains valid "day" sleep information
def get_sleep_df(db_path= 'fitbit_database.db'):
    conn = sqlite3.connect(db_path)

    # Compute sleep duration for each logId and assign it to the first date
    # Load the minute_sleep table
    query_sleep = '''
    SELECT Id, date, value, logId
    FROM minute_sleep
    '''
    df_sleep = pd.read_sql_query(query_sleep, conn)

    # Convert the date column to datetime
    df_sleep['date'] = pd.to_datetime(df_sleep['date'])

    # Group by logId to calculate total sleep duration and first date
    df_sleep_grouped = df_sleep.groupby('logId').agg(
        Id=('Id', 'first'),  # Keep the Id
        TotalSleepDuration=('value', 'count'),  # Count number of minute entries (each row = 1 min)
        FirstDate=('date', 'min'),  # First date in the logId group (start time)
        LastDate=('date', 'max')  # Last date in the logId group (end time)
    ).reset_index()

    # Extract the date from the first timestamp
    df_sleep_grouped['SleepDate'] = df_sleep_grouped['FirstDate'].dt.date

    # Add a new column to check if the sleep is morning sleep 
    # (start time is between 00:00 and 11:00 AM)
    df_sleep_grouped['IsMorningSleep'] = (df_sleep_grouped['FirstDate'].dt.hour >= 0) & (df_sleep_grouped['FirstDate'].dt.hour < 11)

    # Adjust SleepDate: if sleep starts between 00:00 and 11:00 AM, assign it to the previous day
    df_sleep_grouped['SleepDate'] = df_sleep_grouped.apply(
        lambda row: (row['FirstDate'] - pd.Timedelta(days=1)).date() if row['IsMorningSleep'] else row['FirstDate'].date(),
        axis=1
    )

    df_sleep_grouped_sorted = pd.concat([group for _, group in df_sleep_grouped.groupby('Id')])

    aggregated_data = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
        logId=('logId', 'first'),  # First logId in the group
        TotalSleepDuration=('TotalSleepDuration', 'sum'),  # Sum of sleep duration
        FirstDate=('FirstDate', 'min'),  # Minimum FirstDate in the group
        LastDate=('LastDate', 'max'),  # Maximum LastDate in the group
    ).reset_index()

    return aggregated_data



#def analyze_sleep_per_day(user_id, db_path='fitbit_database.db'):

    """
    Calculate the average amount of sleep per day for a specific user.

    Parameters:
        user_id (int): The ID of the user.
        db_path (str): Path to the SQLite database file.

    Returns:
        float: The average sleep duration (in minutes) per day for the user.
    """
    # Step 1: Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Step 2: Query the minute_sleep table for the specific user
    query = f'''
    SELECT Id, date, value
    FROM minute_sleep
    WHERE Id = {user_id}
    '''
    df_sleep = pd.read_sql_query(query, conn)

    # Step 3: Convert the date column to datetime and extract the date
    df_sleep['date'] = pd.to_datetime(df_sleep['date']).dt.date

    # Step 4: Group by date and count the number of rows (minutes) for each date
    df_sleep_grouped = df_sleep.groupby('date').agg(
        TotalSleepMinutes=('value', 'count')
    ).reset_index()

    sleep_stats = df_sleep_grouped.describe()

    conn.close()

    return sleep_stats

# summary sleep statistics for a user
def analyze_sleep(user_id, df):
    """
    Calculate the average amount of sleep per day for a specific user.

    Parameters:
        user_id (int): The ID of the user.
        df (dataframe): Pandas dataframe with logged durations of sleep moments.

    Returns:
        summary (dataframe): The summary of the sleep data for the user.
    """

    user_data = df[df['Id'] == user_id]
    summary = user_data['TotalSleepDuration'].describe()

    return summary

# plot the minutes of sleep for a user
def plot_sleep_minutes(user_id, df):
    """
    Plot a bar plot of sleep minutes for each SleepDate for a specific user.

    Parameters:
        user_id (float or int): The ID of the user.
        df (pd.DataFrame): The DataFrame containing sleep data.
    """
    # Filter the DataFrame for the specific user
    user_data = df[df['Id'] == user_id]

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x='SleepDate', y='TotalSleepDuration', data=user_data, palette='viridis')

    # Add labels and title
    plt.xlabel('Sleep Date')
    plt.ylabel('Total Sleep Minutes')
    plt.title(f'Sleep Minutes per Day for User {user_id}')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Show the plot
    plt.tight_layout()
    plt.show()

# avg sleep of people for the day of the week
def avg_sleep_per_weekday(df, user_id=None):
    
    df['SleepDate'] = pd.to_datetime(df['SleepDate'])
    df['DayOfWeek'] = df['SleepDate'].dt.day_name()

    average_sleep_by_day = df.groupby('DayOfWeek')['TotalSleepDuration'].mean().reset_index()

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    average_sleep_by_day['DayOfWeek'] = pd.Categorical(average_sleep_by_day['DayOfWeek'], categories=day_order, ordered=True)
    average_sleep_by_day = average_sleep_by_day.sort_values('DayOfWeek')

    if user_id is not None:
        user_df = df[df['Id'] == user_id]
        user_average_sleep_by_day = user_df.groupby('DayOfWeek')['TotalSleepDuration'].mean().reset_index()
        user_average_sleep_by_day['DayOfWeek'] = pd.Categorical(user_average_sleep_by_day['DayOfWeek'], categories=day_order, ordered=True)
        user_average_sleep_by_day = user_average_sleep_by_day.sort_values('DayOfWeek')

    # plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='DayOfWeek', y='TotalSleepDuration', data=average_sleep_by_day, palette='viridis')
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Sleep Duration (Minutes)')
    plt.title('Average Sleep Duration by Day of the Week')
    plt.tight_layout()
    plt.show()

    print(average_sleep_by_day)
  
    
def avg_sleep_per_weekday_imp(df, user_id=None):
    df['SleepDate'] = pd.to_datetime(df['SleepDate'])
    df['DayOfWeek'] = df['SleepDate'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    average_sleep_by_day_all = df.groupby('DayOfWeek')['TotalSleepDuration'].mean().reset_index()
    average_sleep_by_day_all['DayOfWeek'] = pd.Categorical(average_sleep_by_day_all['DayOfWeek'], categories=day_order, ordered=True)
    average_sleep_by_day_all = average_sleep_by_day_all.sort_values('DayOfWeek')
    average_sleep_by_day_all['Type'] = 'All Users'  # Add a column to identify this data as "All Users"

    if user_id is not None:
        user_df = df[df['Id'] == user_id]
        if not user_df.empty:
            average_sleep_by_day_user = user_df.groupby('DayOfWeek')['TotalSleepDuration'].mean().reset_index()
            average_sleep_by_day_user['DayOfWeek'] = pd.Categorical(average_sleep_by_day_user['DayOfWeek'], categories=day_order, ordered=True)
            average_sleep_by_day_user = average_sleep_by_day_user.sort_values('DayOfWeek')
            average_sleep_by_day_user['Type'] = f'User {user_id}'  # Add a column to identify this data as "User X"

            combined_df = pd.concat([average_sleep_by_day_all, average_sleep_by_day_user], ignore_index=True)
        else:
            print(f"No data found for user_id: {user_id}")
            combined_df = average_sleep_by_day_all
    else:
        combined_df = average_sleep_by_day_all  

    plt.figure(figsize=(12, 6))
    sns.barplot(x='DayOfWeek', y='TotalSleepDuration', hue='Type', data=combined_df, palette='viridis')
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Sleep Duration (Minutes)')
    plt.title('Average Sleep Duration by Day of the Week')
    plt.legend(title='Dataset')
    plt.tight_layout()
    plt.show()

    print(combined_df)


#Example usage
df_sleep = get_sleep_df()
df_sleep.to_csv(f"df_sleep.txt", sep='\t', index=False)

print(df_sleep)
user_id = 1503960366
stats = analyze_sleep(user_id, df_sleep)

print(f"Summary for the sleep data for user {user_id}:")
print(stats.to_frame().to_markdown())

plot_sleep_minutes(user_id, df_sleep)

avg_sleep_per_weekday(df_sleep)
avg_sleep_per_weekday_imp(df_sleep, user_id)
