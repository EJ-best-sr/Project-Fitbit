import sqlite3
import pandas as pd

def export_weight_log_to_csv(output_filename="weight_log_export.csv"):
    """
    Connects to the Fitbit database, retrieves the weight_log table,
    and exports it to a CSV file.

    Parameters:
    output_filename (str): Name of the output CSV file (default: "weight_log_export.csv").

    Returns:
    None (Saves the CSV file)
    """
    # Connect to the database
    connection = sqlite3.connect("fitbit_database.db")

    # Query to select all data from weight_log
    query = "SELECT * FROM weight_log"
    weight_data = pd.read_sql_query(query, connection)

    # Close database connection
    connection.close()

    # Export to CSV
    weight_data.to_csv(output_filename, index=False)
    
    print(f"weight_log table successfully exported to {output_filename}")

# Call the function to export
export_weight_log_to_csv("C:/Users/Admin/Downloads/weight_log_export.csv")
