import sqlite3
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.stats as stats

# Create the ss1 folder if it doesn't exist
output_folder = 'ss1'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

conn = sqlite3.connect('fitbit_database.db')

sns.set_palette('viridis')

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

df_sleep_grouped_sorted = pd.concat([group for _, group in df_sleep_grouped.groupby('Id')])
df_sleep_grouped_sorted = df_sleep_grouped_sorted.reset_index(drop=True)

# Write entire dataframe to file in the folder
df_sleep_grouped_sorted.to_csv("ss1/df_sleep_grouped.txt", sep='\t', index=False)

# Group by Id and SleepDate to calculate total sleep minutes for each user on each day
df_sleep_aggregated = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
    TotalSleepDuration=('TotalSleepDuration', 'sum')  # Sum of sleep minutes
).reset_index()

df_sleep_aggregated.to_csv("ss1/df_sleep_aggregated.txt", sep='\t', index=False)

# Compute total active minutes for each individual
# Load the daily_activity table
query_activity = '''
SELECT Id, ActivityDate, 
       SedentaryMinutes as TotalSedentaryMinutes
FROM daily_activity
'''
df_activity = pd.read_sql_query(query_activity, conn)

# Convert ActivityDate to datetime and extract the date
df_activity['ActivityDate'] = pd.to_datetime(df_activity['ActivityDate']).dt.date

# Write dataframe to file in the folder
df_activity.to_csv("ss1/df_activity.txt", sep='\t', index=False)

# Merge the dataframes, connect on sleep date and activity date
df_merged = pd.merge(
    df_sleep_aggregated, 
    df_activity, 
    left_on=['Id', 'SleepDate'], 
    right_on=['Id', 'ActivityDate'], 
    how='inner'
)

# Remove the sleep of less than 3 hours
df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

# Write entire dataframe to file in the folder
df_merged_filtered.to_csv("ss1/df_merged.txt", sep='\t', index=False)

# Regression analysis on merged data
X = df_merged_filtered['TotalSedentaryMinutes']  # Independent variable (total active minutes on day 1)
y = df_merged_filtered['TotalSleepDuration']  # Dependent variable (total sleep duration from evening of day 1 to morning of day 2)

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

# Add labels and title
plt.title('QQ-Plot of Residuals', fontsize=16)
plt.xlabel('Theoretical Quantiles of Normal Distribution', fontsize=14)
plt.ylabel('Sample Quantiles', fontsize=14)

plt.show()

conn.close()
