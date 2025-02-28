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
