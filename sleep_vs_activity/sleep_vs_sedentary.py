import sqlite3
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def load_and_process_sleepdata(database_name):
    """
    Load and process data from the database to create the merged DataFrame.
    
    Args:
        database_name (str): Name of the SQLite database.
    
    Returns:
        pd.DataFrame: The merged DataFrame containing sleep and activity data.
    """
    # Connect to the database
    conn = sqlite3.connect(database_name)

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

    # Add a new column to check if the sleep start time is between 00:00 and 11:00 AM
    df_sleep_grouped['IsMorningSleep'] = (df_sleep_grouped['FirstDate'].dt.hour >= 0) & (df_sleep_grouped['FirstDate'].dt.hour < 11)

    # Adjust SleepDate: if sleep starts between 00:00 and 11:00 AM, assign it to the previous day
    df_sleep_grouped['SleepDate'] = df_sleep_grouped.apply(
        lambda row: (row['FirstDate'] - pd.Timedelta(days=1)).date() if row['IsMorningSleep'] else row['FirstDate'].date(),
        axis=1
    )

    # Sort and reset index
    df_sleep_grouped_sorted = pd.concat([group for _, group in df_sleep_grouped.groupby('Id')])
    df_sleep_grouped_sorted = df_sleep_grouped_sorted.reset_index(drop=True)

    # Aggregate sleep data by Id and SleepDate
    df_sleep_aggregated = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
        TotalSleepDuration=('TotalSleepDuration', 'sum'),  # Sum of sleep minutes
        StartTime=('FirstDate', 'min'),  # Earliest FirstDate (start time)
        EndTime=('LastDate', 'max')  # Latest LastDate (end time)
    ).reset_index()

    # Close the database connection
    conn.close()

    return df_sleep_aggregated


def load_and_process_data(database_name):
    """
    Load and process data from the database to create the merged DataFrame.
    
    Args:
        database_name (str): Name of the SQLite database.
    
    Returns:
        pd.DataFrame: The merged DataFrame containing sleep and activity data.
    """
    # Connect to the database
    conn = sqlite3.connect(database_name)

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

    # Add a new column to check if the sleep start time is between 00:00 and 11:00 AM
    df_sleep_grouped['IsMorningSleep'] = (df_sleep_grouped['FirstDate'].dt.hour >= 0) & (df_sleep_grouped['FirstDate'].dt.hour < 11)

    # Adjust SleepDate: if sleep starts between 00:00 and 11:00 AM, assign it to the previous day
    df_sleep_grouped['SleepDate'] = df_sleep_grouped.apply(
        lambda row: (row['FirstDate'] - pd.Timedelta(days=1)).date() if row['IsMorningSleep'] else row['FirstDate'].date(),
        axis=1
    )

    # Sort and reset index
    df_sleep_grouped_sorted = pd.concat([group for _, group in df_sleep_grouped.groupby('Id')])
    df_sleep_grouped_sorted = df_sleep_grouped_sorted.reset_index(drop=True)

    # Aggregate sleep data by Id and SleepDate
    df_sleep_aggregated = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
        TotalSleepDuration=('TotalSleepDuration', 'sum'),  # Sum of sleep minutes
        StartTime=('FirstDate', 'min'),  # Earliest FirstDate (start time)
        EndTime=('LastDate', 'max')  # Latest LastDate (end time)
    ).reset_index()

    # Load the daily_activity table
    query_activity = '''
    SELECT Id, ActivityDate, 
           SedentaryMinutes as TotalSedentaryMinutes
    FROM daily_activity
    '''
    df_activity = pd.read_sql_query(query_activity, conn)

    # Convert ActivityDate to datetime and extract the date
    df_activity['ActivityDate'] = pd.to_datetime(df_activity['ActivityDate']).dt.date

    # Merge the dataframes
    df_merged = pd.merge(
        df_sleep_aggregated, 
        df_activity, 
        left_on=['Id', 'SleepDate'], 
        right_on=['Id', 'ActivityDate'], 
        how='inner'
    )

    # Close the database connection
    conn.close()

    return df_merged


def perform_regression_analysis(df_merged):
    """
    Perform regression analysis on the merged DataFrame.
    
    Args:
        df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.
    """
    # Remove the sleep of less than 3 hours
    df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

    # Regression analysis
    X = df_merged_filtered['TotalSedentaryMinutes']  # Independent variable
    y = df_merged_filtered['TotalSleepDuration']  # Dependent variable

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())

    # Plot the regression results
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_merged_filtered['TotalSedentaryMinutes'], y=df_merged_filtered['TotalSleepDuration'], alpha=0.9)
    sns.regplot(x=df_merged_filtered['TotalSedentaryMinutes'], y=df_merged_filtered['TotalSleepDuration'], scatter=False, color=(43/255, 129/255, 126/255))
    plt.xlabel('Total Sedentary Minutes')
    plt.ylabel('Total Sleep Duration')
    plt.title('Regression: Sedentary Time vs Sleep Time')
    plt.show()

    # Calculate residuals
    residuals = model.resid
    print(f"Number of observations: {len(residuals)}")

    # Plot histogram of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.title('Histogram of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.show()

    # Plot Q-Q plot of residuals
    plt.figure(figsize=(10, 6))
    qq = stats.probplot(residuals, dist="norm", plot=plt)

    points = plt.gca().get_lines()[0]
    line = plt.gca().get_lines()[1] 

    points.set_markerfacecolor((69/255, 86/255, 128/255))  
    points.set_markeredgecolor('black') 
    points.set_markersize(5)           
    line.set_color((44/255, 131/255, 127/255))
    line.set_linestyle('--')   
    line.set_linewidth(2)          

    plt.title('QQ-Plot of Residuals', fontsize=16)
    plt.xlabel('Theoretical Quantiles of Normal Distribution', fontsize=14)
    plt.ylabel('Sample Quantiles', fontsize=14)
    plt.show()


def calculate_user_statistics_sedentary(df_merged, user_id=None, start_date=None, end_date=None):
    """
    Calculate the average sleep minutes and average activity minutes for a specific user or the entire database.
    
    Args:
        df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.
        user_id (int, float, or None): The Id of the user to calculate statistics for. If None, calculates for the entire database.
        start_date (str or None): The start date in 'YYYY-MM-DD' format. If None, calculates from the earliest date.
        end_date (str or None): The end date in 'YYYY-MM-DD' format. If None, calculates up to the latest date.
    
    Returns:
        dict: A dictionary containing the average sleep minutes and average activity minutes, rounded to integers.
    """
    if user_id is not None:
        df_filtered = df_merged[df_merged['Id'] == user_id].copy() 
    else:
        # For the entire database, exclude sleep records with less than 180 minutes
        df_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180].copy()  

    # Convert SleepDate to datetime for filtering
    df_filtered.loc[:, 'SleepDate'] = pd.to_datetime(df_filtered['SleepDate']) 

    if start_date:
        start_date = pd.to_datetime(start_date)
        df_filtered = df_filtered[df_filtered['SleepDate'] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[df_filtered['SleepDate'] <= end_date]


    avg_activity_minutes = df_filtered['TotalSedentaryMinutes'].mean()
    num_records = df_filtered['TotalSedentaryMinutes'].count()
    avg_activity_minutes = round(avg_activity_minutes) if not pd.isna(avg_activity_minutes) else None
    sd_activity_minutes = df_filtered['TotalSedentaryMinutes'].std()


    return avg_activity_minutes, sd_activity_minutes, num_records
    
    
def calculate_user_statistics_sleep(df_merged, user_id=None, start_date=None, end_date=None):
    """
    Calculate the average sleep minutes and average activity minutes for a specific user or the entire database.
    
    Args:
        df_merged (pd.DataFrame): The merged DataFrame containing sleep and activity data.
        user_id (int, float, or None): The Id of the user to calculate statistics for. If None, calculates for the entire database.
        start_date (str or None): The start date in 'YYYY-MM-DD' format. If None, calculates from the earliest date.
        end_date (str or None): The end date in 'YYYY-MM-DD' format. If None, calculates up to the latest date.
    
    Returns:
        dict: A dictionary containing the average sleep minutes and average activity minutes, rounded to integers.
    """
    # Filter by user_id if specified
    if user_id is not None:
        df_filtered = df_merged[df_merged['Id'] == user_id].copy()  
    else:
        # For the entire database, exclude sleep records with less than 180 minutes
        df_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180].copy() 

    df_filtered.loc[:, 'SleepDate'] = pd.to_datetime(df_filtered['SleepDate']) 


    if start_date:
        start_date = pd.to_datetime(start_date)
        df_filtered = df_filtered[df_filtered['SleepDate'] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[df_filtered['SleepDate'] <= end_date]

    avg_sleep_minutes = df_filtered['TotalSleepDuration'].mean()
    num_records = df_filtered['TotalSleepDuration'].count()
    sd_sleep_minutes = df_filtered['TotalSleepDuration'].std()


    avg_sleep_minutes = round(avg_sleep_minutes) if not pd.isna(avg_sleep_minutes) else None

    return avg_sleep_minutes, sd_sleep_minutes, num_records
    
