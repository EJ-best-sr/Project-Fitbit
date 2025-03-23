import sqlite3
import pandas as pd
import statsmodels.api as sm

# Reconnect to the database to fetch the required data
conn = sqlite3.connect("fitbit_database.db")

# Fetch weight log data
weight_query = """
    SELECT Id, Date, WeightKg 
    FROM weight_log
"""
weight_data = pd.read_sql_query(weight_query, conn)

# Fetch daily activity data
activity_query = """
    SELECT Id, ActivityDate, TotalSteps, Calories
    FROM daily_activity
"""
activity_data = pd.read_sql_query(activity_query, conn)

# Close the connection
conn.close()

# Convert Date columns to datetime (Remove time component)
weight_data["Date"] = pd.to_datetime(weight_data["Date"]).dt.date
activity_data["ActivityDate"] = pd.to_datetime(activity_data["ActivityDate"]).dt.date

# Merge activity with weight data
merged_data = activity_data.merge(weight_data, left_on=["Id", "ActivityDate"], right_on=["Id", "Date"], how="left")

# Sort by user and date for proper interpolation
merged_data = merged_data.sort_values(by=["Id", "ActivityDate"])

# ** Fix Interpolation Issue **
merged_data["WeightKg"] = merged_data.groupby("Id")["WeightKg"].apply(lambda group: group.interpolate(method="linear")).reset_index(level=0, drop=True)

# Compute weight change per user
weight_change = merged_data.groupby("Id", as_index=False).agg(
    StartWeight=("WeightKg", "first"),
    EndWeight=("WeightKg", "last")
)
weight_change["WeightChange"] = weight_change["EndWeight"] - weight_change["StartWeight"]

# Compute activity summary per user
activity_summary = merged_data.groupby("Id", as_index=False).agg(
    AvgSteps=("TotalSteps", "mean"),
    AvgCalories=("Calories", "mean")
)

performance_data = pd.merge(weight_change, activity_summary, on="Id", how="inner")

# Remove users with missing weight change data
cleaned_data = performance_data.dropna(subset=["WeightChange"])

if cleaned_data.empty:
    print("No valid data available after cleaning. Regression cannot be performed.")
else:
    # Define independent variables (Avg Steps and Avg Calories)
    X = cleaned_data[["AvgSteps", "AvgCalories"]]

    # Add a constant term for the intercept
    X = sm.add_constant(X)

    # Define dependent variable (Weight Change)
    y = cleaned_data["WeightChange"]

    # Fit the regression model
    model = sm.OLS(y, X).fit()

    # Display regression summary
    print(model.summary())