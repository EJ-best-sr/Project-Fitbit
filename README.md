# Project-Fitbit
## Overview
This project is created to analyze the Fitbit database containg the records of physical activity, sleep, sedentary activity, weight and BMI etc of the users.

## Part 1

Below you can find the description of each function written for Part 1. The example of usage can be found in the `example_main.py` file.

#### `def plot_workout_frequency_by_day(df)`:
Plots the frequency of workouts by day of the week for all the users in the database by creating a barplot with bins for each day of the week.

**Parameters:**
- `df`: The Pandas dataframe of the `daily_activity` table.

#### `plot_distance_per_user`:
Visualizes the total distance traveled by each user from a given dataset by creating a bar plot with bins corresponding to the unique users in the database. 

**Parameters:**
- `df`: The Pandas dataframe of the `daily_activity` table. It must include the following columns:
  - `Id`: Unique identifier for each user.
  - `TotalDistance`: The total distance traveled by the user.

#### `load_data`:
Loads activity data from a CSV file and converts the 'ActivityDate' column to datetime format.

**Parameters:**
- `file_path` (str): The path to the CSV file containing activity data.

**Returns:**
- `pd.DataFrame`: A DataFrame containing the loaded activity data with 'ActivityDate' as a datetime object.

#### `plot_calories_per_day`:
Plots the daily calories burnt for a specific user within an optional date range.

**Parameters:**
- `df` (pd.DataFrame): The DataFrame containing user activity data.
- `user_id` (int): The ID of the user whose calories will be plotted.
- `start_date` (str, optional): The start date for filtering data (YYYY-MM-DD format).
- `end_date` (str, optional): The end date for filtering data (YYYY-MM-DD format).

**Returns:**
- `None`: Displays a matplotlib line chart.

## Part 3


#### `plot_calories_per_4_hour_block`:
Plots the average calories burnt per 4-hour time block.

**Parameters:**
- `None`

**Returns:**
- `None`: Displays a matplotlib bar chart.

#### `visualize_heart_rate_and_intensity`:
Visualizes heart rate and activity intensity for a given user over 8-hour intervals.

**Parameters:**
- `user_id` (int): The ID of the user whose heart rate and activity data will be analyzed.

**Returns:**
- `None`: Displays a matplotlib line chart comparing heart rate and activity intensity.

#### `plot_sleep_per_4_hour_block`:
Plots the average minutes of sleep per 4-hour time block.

**Parameters:**
- `None`

**Returns:**
- `None`: Displays a matplotlib bar chart.

#### `plot_steps_per_4_hour_block`:
Plots the average steps taken per 4-hour time block.

**Parameters:**
- `None`

**Returns:**
- `None`: Displays a matplotlib bar chart.

## Part 4


#### `plot_total_distance_per_day`:
Plots total distance per day for a given user within a specified date range.

**Parameters:**
- `user_id` (int): The ID of the user.
- `start_date` (str): The start date in the format 'MM/DD/YYYY'.
- `end_date` (str): The end date in the format 'MM/DD/YYYY'.

**Returns:**
- `None`: Displays a bar plot of total distance per day for the user.

#### `plot_total_steps_per_day`:
Plots total steps per day for a given user within a specified date range.

**Parameters:**
- `user_id` (int): The ID of the user.
- `start_date` (str): The start date in the format 'MM/DD/YYYY'.
- `end_date` (str): The end date in the format 'MM/DD/YYYY'.

**Returns:**
- `None`: Displays a bar plot of total steps per day for the user.

#### `replace_missing_values_weight_log`:
Retrieves the 'weight_log' table from the database, replaces missing values in the 'WeightKg' column with the equivalent weight in kilograms based on the 'WeightPounds' column, and returns a copy of the modified data without altering the original database.

**Parameters:**
- `None`

**Returns:**
- `pd.DataFrame`: A copy of the 'weight_log' table with updated 'WeightKg' values where NaN values are replaced by the conversion from 'WeightPounds' to 'WeightKg'.

#### `get_4_hour_sleep_blocks`
Retrieves and plots the user's sleep data in 4-hour blocks (0-4 AM, 4-8 AM, 8-12 PM, 12-4 PM, etc.) for a specific date.

**Parameters:**
- `user_id (float)`: The user's ID.
- `date (str)`: The date in "MM/DD/YYYY" format.

**Returns:**
- `pandas.DataFrame`: A DataFrame with 4-hour blocks and the total sleep minutes in each block.

#### `heart_rate_analysis`
Analyzes heart rate variability metrics (RMSSD, SDNN, PNN50) for a given user ID. This function calculates and returns various heart rate statistics based on the user's heart rate data.

**Parameters:**
- `user_id (int)`: The ID of the user whose heart rate data will be analyzed.

**Returns:**
- `pandas.DataFrame`: A DataFrame containing the user ID and the calculated heart rate variability metrics (RMSSD, SDNN, PNN50).
