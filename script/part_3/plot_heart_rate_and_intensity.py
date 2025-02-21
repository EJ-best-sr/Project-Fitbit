import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/fitbit_database.db")

def visualize_heart_rate_and_intensity(user_id):
    # Fetch heart rate data
    query_heart_rate = f"SELECT Time, Value FROM heart_rate WHERE Id= {user_id}"
    heart_rate = pd.read_sql_query(query_heart_rate, conn) 
    heart_rate["Time"] = pd.to_datetime(heart_rate["Time"])

    # Resample to 8-hour intervals and calculate the mean
    heart_rate_8h = heart_rate.resample('8H', on='Time').mean().reset_index()

    # Fetch intensity data
    query_intensity = f"SELECT ActivityHour, TotalIntensity FROM hourly_intensity WHERE Id= {user_id}"
    total_intensity = pd.read_sql_query(query_intensity, conn)
    total_intensity["ActivityHour"] = pd.to_datetime(total_intensity["ActivityHour"])

    # Resample intensity data to 8-hour intervals and calculate the mean
    total_intensity_8h = total_intensity.resample('8H', on='ActivityHour').mean().reset_index()

    # Create a range of unique 8-hour timestamps present in both datasets
    all_hours = pd.date_range(
        start=max(heart_rate_8h["Time"].min(), total_intensity_8h["ActivityHour"].min()), 
        end=min(heart_rate_8h["Time"].max(), total_intensity_8h["ActivityHour"].max()), 
        freq="8H"
    )

    # Create a DataFrame to provide a full reference timeline
    time_df = pd.DataFrame({"Time": all_hours})

    # Merge the dataframes based on the complete timeline
    merged_df = time_df.merge(heart_rate_8h, on="Time", how="left").merge(
        total_intensity_8h, left_on="Time", right_on="ActivityHour", how="left"
    )

    # Drop the extra time column (ActivityHour) since "Time" is now the standard
    merged_df.drop(columns=["ActivityHour"], inplace=True)

    # Drop any rows with NaN values resulting from missing data in the overlap
    merged_df.dropna(inplace=True)

    # Set Seaborn style and use the Viridis color palette
    sns.set(style="whitegrid")  # Using darkgrid for the plot style
    palette = sns.color_palette("viridis", as_cmap=True)  # Viridis color palette as a colormap

    # Plot the data
    plt.figure(figsize=(14, 7))

    # Plot "Value" (Heart Rate) using the first color from the Viridis palette
    sns.lineplot(data=merged_df, x="Time", y="Value", label="Heart Rate (Value)", marker="o", color=palette(0.1))

    # Plot "TotalIntensity" (Activity) using the last color from the Viridis palette
    sns.lineplot(data=merged_df, x="Time", y="TotalIntensity", label="Activity (TotalIntensity)", marker="o", color=palette(0.5))

    # Enhance plot with styling
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Value", fontsize=14)
    plt.title("Heart Rate and Activity per 8 Hours", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    

    # Display the legend
    plt.legend()

    # Tight layout to adjust plot spacing
    plt.tight_layout()

    # Show the plot
    plt.show()
