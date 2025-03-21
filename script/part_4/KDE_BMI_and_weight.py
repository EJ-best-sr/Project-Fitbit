import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_kde_bmi_weight():
    """
    Generates KDE plots for BMI and Weight, categorized by user classification.

    Returns:
    None (Displays KDE plots)
    """
    # Connect to the database
    conn = sqlite3.connect("fitbit_database.db")

    # Load weight_log table
    weight_log = pd.read_sql_query("SELECT Id, WeightKg, BMI FROM weight_log", conn)

    # Load user classification data
    user_classification_query = """
        SELECT Id, 
               CASE 
                   WHEN COUNT(ActivityDate) <= 10 THEN 'Light User'
                   WHEN COUNT(ActivityDate) BETWEEN 11 AND 15 THEN 'Moderate User'
                   ELSE 'Heavy User'
               END AS Class
        FROM daily_activity
        GROUP BY Id
    """
    user_classification_df = pd.read_sql_query(user_classification_query, conn)

    # Close the connection
    conn.close()

    # Merge weight data with user classification
    merged_data = weight_log.merge(user_classification_df, on="Id", how="left")

    # Set figure size
    plt.figure(figsize=(12, 6))

    # KDE Plot for BMI
    plt.subplot(1, 2, 1)
    sns.kdeplot(data=merged_data, x="BMI", hue="Class", fill=True, common_norm=False, palette="Set1")
    plt.title("KDE of BMI by User Class")
    plt.xlabel("BMI")
    plt.ylabel("Density")

    # KDE Plot for Weight
    plt.subplot(1, 2, 2)
    sns.kdeplot(data=merged_data, x="WeightKg", hue="Class", fill=True, common_norm=False, palette="Set2")
    plt.title("KDE of Weight by User Class")
    plt.xlabel("Weight (Kg)")
    plt.ylabel("Density")

    # Show the plots
    plt.tight_layout()
    plt.show()

# Call the function to generate KDE plots
plot_kde_bmi_weight()