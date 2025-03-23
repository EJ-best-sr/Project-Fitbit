# Project-Fitbit
[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red?logo=streamlit&labelColor=black)](https://streamlit.io/)
![pandas](https://img.shields.io/badge/pandas-2.2.3-lightgrey?logo=pandas)
![numpy](https://img.shields.io/badge/numpy-2.2.4-blue?logo=numpy)
![scipy](https://img.shields.io/badge/scipy-1.11.2-blue?logo=scipy)
![matplotlib](https://img.shields.io/badge/matplotlib-3.8.0-orange?logo=matplotlib)
![plotly](https://img.shields.io/badge/plotly-5.17.0-9cf?logo=plotly)
![seaborn](https://img.shields.io/badge/seaborn-0.12.2-lightblue?logo=seaborn)
![statsmodels](https://img.shields.io/badge/statsmodels-0.14.0-brown?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%3E%3D1.3.2-blue?logo=scikit-learn)
## 📋 Project Overview:
This project focuses on analyzing Fitbit data collected from 35 participants in a 2016 Amazon survey. The goal is to develop an interactive Streamlit dashboard that presents various key metrics such as:
- Daily steps, distance, and calories burned
- Sleep patterns and duration
- Sedentary activity
- Weight and BMI insights
- Weather correlation with Fitbit activity data

The dashboard is designed for studying Fitbit data trends, participants who want to explore their activity statistics, and people in general who want to understand what insights can be derived from Fitbit data.
## 📦 Dependencies
This project relies on several python libraries for data processing and visualization, which are listed in the `requirements.txt` file.
## 📁 Project Structure
The main files and directories in this repository are:
<pre>   Project-Fitbit/
├── .devcontainer/ # Development container setup
├── data/ # All data for the project
├── general/ # Chart and Analysis in "General Page"
├── sleep_vs_activity/ # Sleep and activity comparison
├── user_spec/ # User-specific plots
├── dashboard.py # Main Fitbit dashboard
├── image.png # Dashboard preview image (if applicable)
├── legacy/ # All working tasks from part 1 -> 4
├── requirements.txt # Python dependencies
├── README.md # Project overview   </pre>
### Clarification of Project Structure
- The `general/` folder contains all the plots used for the **General Information** page, including its subpages: [`Home`, `Regression Analysis`, `Weekday Analysis`, and `Weather Analysis`].
- The `sleep_vs_activity/` folder provides an additional plot specifically for the `Regression Analysis` subpage.
- The `user_spec/` folder includes all plots related to the **User-Specific** page. Each plot generally takes three parameters: `start date`, `end date`, and `Id`, allowing users to filter results by user and time range.
- The `dashboard.py` file serves as the main entry point of the Fitbit dashboard. It imports and integrates all functions and plots from the folders mentioned above.
- The `legacy/` folder contains exploratory data analysis work from Parts 1 to 4, which formed the foundation for developing the dashboard.
- Finally, the `README.md` file gives a clean and clear description of the project and its structure.


### Dashboard example:


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

change

---------------------------------------------------------------------

## General Information 

### Home 

#### Overall Statistics 

##### Number of Users, Average Distance, Average Calories:

----

##### Average Sleep Duration 

----

##### Average Sedentary Minutes

----

##### Average Weight, Height and BMI

The preprocessing function for this numerical calculation can be found in the `general` folder, in the file: `height_and_weight_metrics.py`.

----
##### Average Steps

----



----

#### Overall Graphical Analysis

##### Total Distance per User

----

##### Average Calories Burned per Total Steps

----

##### Weight vs. Calories Burned

----

#### Overview of User Health and Activity Patterns

##### Number of Days Using Fitbit

----

##### Active Minutes by Intensity

-----

##### BMI Classification

----

### Regression Analysis

#### Sedentary Time vs Sleep Time Analysis

##### Regression: Sedentary Time vs Sleep Time

----

##### Histogram of Residuals (Density-Scaled)

-----

##### Q-Q Plot of Residuals

-----
##### Sedentary Minutes vs BMI and Total Active Minutes vs BMI

#### Calories Burned vs Steps

##### Calories Burned vs Steps

-----

### Weekday Analysis

##### Box plot: Total Distance per Day of the Week

----

##### Box plot: Sedentary Activity per Day of the Week

----

### 4-Hour Block Analysis

##### Average Calories Burnt per 4-Hour Block

The function for this figure can be found in the `general` folder, in the file: `calories_4_hour_blocks_general.py`.

##### Average Minutes of Sleep per 4-Hour Block

The function for this figure can be found in the `general` folder, in the file: `sleep_4_hour_blocks_general.py`.

##### Average Steps per 4-Hour Block

The function for this figure can be found in the `general` folder, in the file: `steps_4_hour_blocks_general.py`.

### Weather Analysis

##### Daily and Cumulative Precipitation:

----

##### Heatmap for correlation matrix:

----

##### Box Plot: Total Steps on Rainy vs Non-Rainy Days

----

##### Linear Regression: Total Steps vs Temperature

----

## User-Specific Analysis

#### Numerical Summary

##### Average Distance

---

##### Average Calories

---

##### Average Sleep Duration

---

##### Average Sedentary Minutes

---

##### Last Weight 

The preprocessing function for this numerical calculation can be found in the `general` folder, in the file: `height_and_weight_metrics.py`.

##### Last Height 

The preprocessing function for this numerical calculation can be found in the `general` folder, in the file: `height_and_weight_metrics.py`.

##### Average Steps

---

##### Comparison for this date range:

----

##### Total Steps and Total Distance per Day

The function for this figure can be found in the `user_spec` folder, in the file:
`steps_and_distance_user.py`.

##### Calories Burnt per Day

The function for this figure can be found in the `user_spec` folder, in the file:
`calories_user.py`.

##### Very Active, Fairly Active, and Lightly Active Minutes Proportions

-----

##### Total Active Minutes versus Sedentary Activity

-----

##### Calories vs Steps Regression

-----

##### Heart rate analysis

The function for these numerical calculations can be found in the `user_spec` folder, in the file: `heart_analysis_user.py`.
