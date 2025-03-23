import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bmi_distribution():
    """
    Fetches BMI data from the Fitbit database and plots a histogram showing
    the distribution of BMI values.
    
    Parameters:
    None
    
    Returns:
    None
    """
    # Connect to the database
    connection = sqlite3.connect("fitbit_database.db")
    
    # Query weight_log table to get BMI values
    query = "SELECT BMI FROM weight_log"
    weight_data = pd.read_sql_query(query, connection)
    
    # Close database connection
    connection.close()
    
    # Drop missing BMI values
    weight_data.dropna(inplace=True)
    
    # Create BMI Distribution Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(weight_data["BMI"], bins=30, kde=True, color='royalblue')

    # Add BMI category reference lines
    plt.axvline(x=18.5, color='green', linestyle='dashed', label="Underweight (18.5)")
    plt.axvline(x=24.9, color='blue', linestyle='dashed', label="Normal (18.5 - 24.9)")
    plt.axvline(x=29.9, color='orange', linestyle='dashed', label="Overweight (25 - 29.9)")
    plt.axvline(x=30, color='red', linestyle='dashed', label="Obese (30+)")

    # Labels and title
    plt.xlabel("BMI")
    plt.ylabel("Frequency")
    plt.title("BMI Distribution of Fitbit Users")
    plt.legend()
    plt.grid(True)
    
    # Show plot
    plt.show()

# Call the function to generate the histogram
plot_bmi_distribution()