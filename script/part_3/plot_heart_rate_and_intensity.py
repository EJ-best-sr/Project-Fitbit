import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

connection = sqlite3.connect("data/fitbit_database.db")

def visualize_heart_rate_and_intensity(user_id):
    """
    Visualizes heart rate and activity intensity for a given user over 8-hour intervals.

    Parameters:
        user_id (int): The ID of the user whose heart rate and activity data will be analyzed.

    Returns:
        None (Displays a matplotlib line chart comparing heart rate and activity intensity)
    """
    query_heart_rate = f"SELECT Time, Value FROM heart_rate WHERE Id= {user_id}"
    heart_rate = pd.read_sql_query(query_heart_rate, connection) 
    heart_rate["Time"] = pd.to_datetime(heart_rate["Time"])
    heart_rate_8h = heart_rate.resample('8H', on='Time').mean().reset_index()

    query_intensity = f"SELECT ActivityHour, TotalIntensity FROM hourly_intensity WHERE Id= {user_id}"
    total_intensity = pd.read_sql_query(query_intensity, connection)
    total_intensity["ActivityHour"] = pd.to_datetime(total_intensity["ActivityHour"])
    total_intensity_8h = total_intensity.resample('8H', on='ActivityHour').mean().reset_index()

    all_hours = pd.date_range(
        start=max(heart_rate_8h["Time"].min(), total_intensity_8h["ActivityHour"].min()), 
        end=min(heart_rate_8h["Time"].max(), total_intensity_8h["ActivityHour"].max()), 
        freq="8H"
    )

    time_df = pd.DataFrame({"Time": all_hours})
    merged_df = time_df.merge(heart_rate_8h, on="Time", how="left").merge(
        total_intensity_8h, left_on="Time", right_on="ActivityHour", how="left"
    )
    merged_df.drop(columns=["ActivityHour"], inplace=True)
    merged_df.dropna(inplace=True)

    sns.set(style="whitegrid")
    palette = sns.color_palette("viridis", as_cmap=True)

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=merged_df, x="Time", y="Value", label="Heart Rate (Value)", marker="o", color=palette(0.1))
    sns.lineplot(data=merged_df, x="Time", y="TotalIntensity", label="Activity (TotalIntensity)", marker="o", color=palette(0.5))

    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Value", fontsize=14)
    plt.title("Heart Rate and Activity per 8 Hours", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.show()

