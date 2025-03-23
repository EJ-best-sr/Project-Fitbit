import sqlite3
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create the sleep_vs_activity folder if it doesn't exist
output_folder = 'sleep_vs_activity'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

sns.set_palette("viridis")

conn = sqlite3.connect('fitbit_database.db')

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
df_sleep_grouped_sorted = df_sleep_grouped_sorted.reset_index(drop=True)

# Write entire dataframe to file in the output_folder folder
df_sleep_grouped_sorted.to_csv(f"{output_folder}/df_sleep_grouped.txt", sep='\t', index=False)

# Group by Id and SleepDate to calculate total sleep minutes for each user on each day
df_sleep_aggregated = df_sleep_grouped_sorted.groupby(['Id', 'SleepDate']).agg(
    TotalSleepDuration=('TotalSleepDuration', 'sum')  # Sum of sleep minutes
).reset_index()

df_sleep_aggregated.to_csv(f"{output_folder}/df_sleep_aggregated.txt", sep='\t', index=False)

# Compute total active minutes for each individual
# Load the daily_activity table
query_activity = '''
SELECT Id, ActivityDate, 
       (VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) as TotalActiveMinutes
FROM daily_activity
'''
df_activity = pd.read_sql_query(query_activity, conn)

# Convert ActivityDate to datetime and extract the date
df_activity['ActivityDate'] = pd.to_datetime(df_activity['ActivityDate']).dt.date

# Write entire dataframe to file in the try6 folder
df_activity.to_csv(f"{output_folder}/df_activity.txt", sep='\t', index=False)

# Merge sleep duration and active minutes data
# Sleep from evening of day 1 to morning of day 2 corresponds to activity on day 1
df_merged = pd.merge(
    df_sleep_aggregated, 
    df_activity, 
    left_on=['Id', 'SleepDate'], 
    right_on=['Id', 'ActivityDate'], 
    how='inner'
)

df_merged_filtered = df_merged[df_merged['TotalSleepDuration'] >= 180]

# Write entire dataframe to file in the folder
df_merged_filtered.to_csv(f"{output_folder}/df_merged.txt", sep='\t', index=False)

# Perform regression analysis on merged data
X = df_merged_filtered['TotalActiveMinutes']  # Independent variable (total active minutes on day 1)
y = df_merged_filtered['TotalSleepDuration']  # Dependent variable (total sleep duration from evening of day 1 to morning of day 2)

# Add a constant to the independent variable
X = sm.add_constant(X)
# Fit the regression model
model = sm.OLS(y, X).fit()
# Print the regression results
print(model.summary())

# Save regression results to a text file in the folder
with open(f"{output_folder}/regression_results.txt", "w") as f:
    f.write(model.summary().as_text())

# Visualize the regression results
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_merged_filtered['TotalActiveMinutes'], y=df_merged_filtered['TotalSleepDuration'], alpha=0.9)
sns.regplot(x=df_merged_filtered['TotalActiveMinutes'], y=df_merged_filtered['TotalSleepDuration'], scatter=False, color=(44/255, 131/255, 127/255))
plt.xlabel('Total Active Minutes (Day 1)')
plt.ylabel('Total Sleep Duration (Evening of Day 1 to Morning of Day 2)')
plt.title('Regression: Activity on Day 1 Predicts Sleep from Evening of Day 1 to Morning of Day 2')

# Save the plot to a file in the folder
plt.savefig(f"{output_folder}/regression_plot.png")

# Show the plot
plt.show()


conn.close()
