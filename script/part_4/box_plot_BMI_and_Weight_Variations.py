import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from classification import classify_users  # Import the classification function

# Fetch user classifications
user_classification_df = classify_users()

# Connect to the database to get weight_log data
conn = sqlite3.connect("fitbit_database.db")

# Load weight_log table
weight_log = pd.read_sql_query("SELECT Id, WeightKg, BMI FROM weight_log", conn)

# Close database connection
conn.close()

# Merge weight data with user classification
merged_data = weight_log.merge(user_classification_df, on="Id", how="left")

# Set figure size
plt.figure(figsize=(12, 6))

# Boxplot for BMI variations grouped by user class
plt.subplot(1, 2, 1)
sns.boxplot(x=merged_data["Class"], y=merged_data["BMI"], palette="Blues")
plt.title("BMI Variations by User Class")
plt.xlabel("User Classification")
plt.ylabel("BMI")

# Boxplot for Weight variations grouped by user class
plt.subplot(1, 2, 2)
sns.boxplot(x=merged_data["Class"], y=merged_data["WeightKg"], palette="Reds")
plt.title("Weight Variations by User Class")
plt.xlabel("User Classification")
plt.ylabel("Weight (Kg)")

# Adjust layout and show the plots
plt.tight_layout()
plt.show()