from sklearn.linear_model import Ridge
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
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

# Merge activity with weight data using an outer join to include more users
merged_data = activity_data.merge(weight_data, left_on=["Id", "ActivityDate"], right_on=["Id", "Date"], how="outer")

# Sort by user and date for proper interpolation
merged_data = merged_data.sort_values(by=["Id", "ActivityDate"])

# Interpolate missing weight values for each user
merged_data["WeightKg"] = merged_data.groupby("Id")["WeightKg"].apply(lambda group: group.interpolate(method="linear")).reset_index(level=0, drop=True)

# Compute activity summary per user
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

# Fill missing values in other columns with median
cleaned_data.fillna(cleaned_data.median(), inplace=True)

# Define independent variables (Steps, Calories, Sleep, Heart Rate, Active Minutes)
X_nonlinear = cleaned_data[["AvgSteps", "AvgCalories", "AvgSedentaryMinutes", "AvgVeryActiveMinutes", "AvgLightlyActiveMinutes", "AvgSleepMinutes", "AvgHeartRate"]]

# Define dependent variable (Avg Weight)
y_nonlinear = cleaned_data["AvgWeight"]
# Standardize features for better regression stability
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_nonlinear)

# Perform feature selection to keep only the best predictors
selector = SelectKBest(score_func=f_regression, k=4)  # Select top 4 best features
X_selected = selector.fit_transform(X_scaled, y_nonlinear)

# Get the names of the selected features
selected_features = X_nonlinear.columns[selector.get_support()]

# Re-run polynomial regression with selected features
X_selected_df = pd.DataFrame(X_selected, columns=selected_features)

# Fit a Ridge Regression model to prevent overfitting
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_selected_df, y_nonlinear)

# Generate predictions
predicted_y_ridge = ridge_model.predict(X_selected_df)

# Scatter Plots with Ridge Regression Fit
plt.figure(figsize=(12, 8))

# Ridge Regression: Best Feature 1 vs. Weight
plt.subplot(2, 2, 1)
sns.scatterplot(x=X_selected_df[selected_features[0]], y=y_nonlinear, color="blue", label="Actual Data")
sns.lineplot(x=X_selected_df[selected_features[0]], y=predicted_y_ridge, color="red", label="Ridge Regression Fit")
plt.xlabel(selected_features[0])
plt.ylabel("Average Weight (Kg)")
plt.title(f"Ridge Regression: {selected_features[0]} vs. Weight")

# Ridge Regression: Best Feature 2 vs. Weight
plt.subplot(2, 2, 2)
sns.scatterplot(x=X_selected_df[selected_features[1]], y=y_nonlinear, color="blue", label="Actual Data")
sns.lineplot(x=X_selected_df[selected_features[1]], y=predicted_y_ridge, color="red", label="Ridge Regression Fit")
plt.xlabel(selected_features[1])
plt.ylabel("Average Weight (Kg)")
plt.title(f"Ridge Regression: {selected_features[1]} vs. Weight")

# Ridge Regression: Best Feature 3 vs. Weight
plt.subplot(2, 2, 3)
sns.scatterplot(x=X_selected_df[selected_features[2]], y=y_nonlinear, color="blue", label="Actual Data")
sns.lineplot(x=X_selected_df[selected_features[2]], y=predicted_y_ridge, color="red", label="Ridge Regression Fit")
plt.xlabel(selected_features[2])
plt.ylabel("Average Weight (Kg)")
plt.title(f"Ridge Regression: {selected_features[2]} vs. Weight")

# Ridge Regression: Best Feature 4 vs. Weight
plt.subplot(2, 2, 4)
sns.scatterplot(x=X_selected_df[selected_features[3]], y=y_nonlinear, color="blue", label="Actual Data")
sns.lineplot(x=X_selected_df[selected_features[3]], y=predicted_y_ridge, color="red", label="Ridge Regression Fit")
plt.xlabel(selected_features[3])
plt.ylabel("Average Weight (Kg)")
plt.title(f"Ridge Regression: {selected_features[3]} vs. Weight")

# Show plots
plt.tight_layout()
plt.show()

# Display R-squared score for model performance
ridge_r_squared = ridge_model.score(X_selected_df, y_nonlinear)
selected_features, ridge_r_squared