import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def plot_weight_vs_activity_all_users():
    """
    Plots a scatter plot of Weight (Kg) vs. Physical Activity (Total Steps & Calories)
    for all Fitbit users in the database.

    Returns:
    None (Displays a scatter plot)
    """
    # Connect to the database
    conn = sqlite3.connect("fitbit_database.db")

    # Query weight_log table for all users
    weight_query = """
        SELECT Id, Date, WeightKg 
        FROM weight_log
    """
    weight_data = pd.read_sql_query(weight_query, conn)

    # Query daily_activity table for all users
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

    # Merge data on Id and Date (now both are pure dates)
    merged_data = weight_data.merge(activity_data, left_on=["Id", "Date"], right_on=["Id", "ActivityDate"], how="inner")

    # Check if there is data available
    if merged_data.empty:
        print("No matching data available for any users.")
        return

    # Plot the scatter plot
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(x=merged_data["TotalSteps"], y=merged_data["WeightKg"],
                              hue=merged_data["Calories"], palette="coolwarm", size=merged_data["Calories"], sizes=(20, 200))

    plt.xlabel("Total Steps")
    plt.ylabel("Weight (Kg)")
    plt.title("Weight vs. Physical Activity for All Users")
    plt.legend(title="Calories Burned", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)

    # Show the plot
    plt.show()

# Call the function to generate the scatter plot for all users
plot_weight_vs_activity_all_users()