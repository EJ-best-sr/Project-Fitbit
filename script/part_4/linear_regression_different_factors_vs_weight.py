import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandas as pd
# Reconnect to the database to fetch additional data with improved merging strategy
conn = sqlite3.connect("fitbit_database.db")

# Fetch daily activity data
activity_query = """
    SELECT Id, ActivityDate, TotalSteps, Calories, SedentaryMinutes, VeryActiveMinutes, LightlyActiveMinutes
    FROM daily_activity
"""
activity_data = pd.read_sql_query(activity_query, conn)

# Fetch weight log data
weight_query = """
    SELECT Id, Date, WeightKg 
    FROM weight_log
"""
weight_data = pd.read_sql_query(weight_query, conn)

# Fetch sleep data
sleep_query = """
    SELECT Id, AVG(value) AS AvgSleepMinutes
    FROM minute_sleep
    GROUP BY Id
"""
sleep_data = pd.read_sql_query(sleep_query, conn)

# Fetch heart rate data
heart_rate_query = """
    SELECT Id, AVG(value) AS AvgHeartRate
    FROM heart_rate
    GROUP BY Id
"""
heart_rate_data = pd.read_sql_query(heart_rate_query, conn)

# Close the connection
conn.close()

# Convert Date columns to datetime (Remove time component)
weight_data["Date"] = pd.to_datetime(weight_data["Date"]).dt.date
activity_data["ActivityDate"] = pd.to_datetime(activity_data["ActivityDate"]).dt.date

# Merge activity with weight data using an outer join to preserve more users
merged_data = activity_data.merge(weight_data, left_on=["Id", "ActivityDate"], right_on=["Id", "Date"], how="outer")

# Sort by user and date for proper interpolation
merged_data = merged_data.sort_values(by=["Id", "ActivityDate"])

# Interpolate missing weight values for each user
merged_data["WeightKg"] = merged_data.groupby("Id")["WeightKg"].apply(lambda group: group.interpolate(method="linear")).reset_index(level=0, drop=True)

# Compute activity summary per user using an outer join to include more users
activity_summary = merged_data.groupby("Id", as_index=False).agg(
    AvgSteps=("TotalSteps", "mean"),
    AvgCalories=("Calories", "mean"),
    AvgSedentaryMinutes=("SedentaryMinutes", "mean"),
    AvgVeryActiveMinutes=("VeryActiveMinutes", "mean"),
    AvgLightlyActiveMinutes=("LightlyActiveMinutes", "mean"),
    AvgWeight=("WeightKg", "mean")  # Avg weight instead of weight change
)

# Merge additional datasets using outer join to include all users
performance_data = activity_summary.merge(sleep_data, on="Id", how="outer")
performance_data = performance_data.merge(heart_rate_data, on="Id", how="outer")

# Remove users with missing AvgWeight only
cleaned_data = performance_data.dropna(subset=["AvgWeight"])
# Fill missing sleep and heart rate data with median values
cleaned_data["AvgSleepMinutes"].fillna(cleaned_data["AvgSleepMinutes"].median(), inplace=True)
cleaned_data["AvgHeartRate"].fillna(cleaned_data["AvgHeartRate"].median(), inplace=True)
# Scatter Plot of Weight vs Key Activity Metrics
plt.figure(figsize=(15, 10))

# Regression of Weight vs. Steps
plt.subplot(2, 2, 1)
sns.regplot(x=cleaned_data["AvgSteps"], y=cleaned_data["AvgWeight"], scatter=True, line_kws={"color": "red"})
plt.xlabel("Average Steps per Day")
plt.ylabel("Average Weight (Kg)")
plt.title("Linear Regression: Steps vs. Weight")

# Regression of Weight vs. Calories
plt.subplot(2, 2, 2)
sns.regplot(x=cleaned_data["AvgCalories"], y=cleaned_data["AvgWeight"], scatter=True, line_kws={"color": "red"})
plt.xlabel("Average Calories Burned per Day")
plt.ylabel("Average Weight (Kg)")
plt.title("Linear Regression: Calories vs. Weight")

# Regression of Weight vs. Sleep
plt.subplot(2, 2, 3)
sns.regplot(x=cleaned_data["AvgSleepMinutes"], y=cleaned_data["AvgWeight"], scatter=True, line_kws={"color": "red"})
plt.xlabel("Average Sleep Minutes per Day")
plt.ylabel("Average Weight (Kg)")
plt.title("Linear Regression: Sleep vs. Weight")

# Regression of Weight vs. Heart Rate
plt.subplot(2, 2, 4)
sns.regplot(x=cleaned_data["AvgHeartRate"], y=cleaned_data["AvgWeight"], scatter=True, line_kws={"color": "red"})
plt.xlabel("Average Heart Rate")
plt.ylabel("Average Weight (Kg)")
plt.title("Linear Regression: Heart Rate vs. Weight")

# Show plots
plt.tight_layout()
plt.show()