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
<pre>   Project-Fitbit/ ├── .devcontainer/ # Dev container setup for reproducibility
├── .streamlit/ # Streamlit configuration and background tweaks
├── data/ # Fitbit and weather data files
├── general/ # Shared plots (e.g., BMI, calories, steps) and regressions
├── sleep_vs_activity/ # Sleep duration vs activity analysis
├── user_spec/ # User-specific charts, regressions, and metrics
├── legacy/ # Scripts from earlier phases (Part 1–4)
├── dashboard.py # 💻 Main Streamlit app — ties everything together
├── requirements.txt # Python dependencies (Plotly, Pandas, etc.)
├── README.md # Project documentation  </pre>
### Clarification of Project Structure
- The `general/` folder contains all the plots used for the **General Information** page, including its subpages: [`Home`, `Regression Analysis`, `Weekday Analysis`, and `Weather Analysis`].
- The `sleep_vs_activity/` folder provides an additional plot specifically for the `Regression Analysis` subpage.
- The `user_spec/` folder includes all plots related to the **User-Specific** page. Each plot generally takes three parameters: `start date`, `end date`, and `Id`, allowing users to filter results by user and time range.
- The `dashboard.py` file serves as the main entry point of the Fitbit dashboard. It imports and integrates all functions and plots from the folders mentioned above.
- The `legacy/` folder contains exploratory data analysis work from Parts 1 to 4, which formed the foundation for developing the dashboard.
- Finally, the `README.md` file gives a clean and clear description of the project and its structure.

## 🚀 Dashboard feature:
- 📌 **Two Main Views**:  
  - **General Information**: Overview of all users with aggregated stats and visuals.  
  - **User-Specific Analysis**: Interactive filters for personalized insights by user and date.

- 📈 **Regression Analysis**:  
  - Multiple linear regressions (e.g., Calories vs Steps, Sleep vs Activity, BMI vs Activity).  
  - Includes R² values, p-values, and statistical interpretation via tooltips:`?` icon at the right of all linear regression plots

- 🗓️ **Weekday & Time-Block Breakdown**:  
  - Box plots and bar charts showing variation across days and 4-hour time blocks.  
  - Built-in significance testing (Kruskal-Wallis) for group comparisons.

- 🌦️ **Weather Impact Analysis**:  
  - Integrates Fitbit data with Chicago weather data. 
  - Compares steps on rainy vs. non-rainy days, and performs temperature-step regression.  
  - Correlation heatmap between weather and health metrics.

- 🧍‍♂️ **User-Centric Visualizations**:  
  - Tracks individual trends in activity, calories, heart rate, BMI, etc.  
  - Dynamic summaries and comparisons to population averages.

- 🎨 **Modern UI**:  
  - Clean layout with responsive columns.  
  - Expandable insights, interactive charts (Plotly), and helpful tooltips.  




## 🧩 Dashboard Components Reference

This section outlines each component of the dashboard and where its logic is implemented in the codebase.

---

### General Information

####  Overall Statistics

- **Number of Users, Average Distance, Calories, Sleep, Weight, Height, BMI, Steps**
  - Source: `dashboard.py` – under the `"Home"` section
  - BMI/Height/Weight preprocessed in: `general/height_and_weight_metrics.py`

#### Overall Graphical Analysis

- **Total Distance per User**
  - `general/total_distances.py`
- **Average Calories Burned per Total Steps**
  - `general/avg_calories_per_step_bins.py`
- **Weight vs Calories Burned**
  - `general/plot_weight_activity.py`

#### User Health and Activity Patterns

- **Days of Fitbit Usage**
  - `general/plot_fitbit_usage.py`
- **Active Minutes by Intensity**
  - `general/pie_chart_minutes.py`
- **BMI Classification**
  - `general/plot_bmi_pie_chart.py`

---

###  Regression Analysis

- **Sedentary Time vs Sleep Time Regression**
  - `general/sleep_regression_analysis.py`
- **Calories Burned vs Steps**
  - `general/calories_vs_steps.py`
- **Sleep vs Activity**
  - `general/sleep_vs_activity.py`
- **BMI vs Sedentary/Active Minutes**
  - `general/bmi_vs_total_active_minutes.py`

---

###  Weekday Analysis

- **Total Distance & Sedentary Minutes by Weekday**
  - Distance: `general/investigate_total_distance_days.py`
  - Sedentary: `general/sedentary_plot_per_day.py`
- **Statistical Testing**
  - `general/distances_kruskal.py` and `general/sedentary_kruskal.py`

---

###  4-Hour Block Analysis

- **Calories Burnt:** `general/calories_4_hour_blocks_general.py`  
- **Sleep:** `general/sleep_4_hour_blocks_general.py`  
- **Steps:** `general/steps_4_hour_blocks_general.py`

---

###  Weather Analysis

- **Precipitation Chart:** `general/weather_Chicago_charts.py`  
- **Steps on Rainy vs Non-Rainy Days:** `general/plot_steps_rainy_or_not.py`  
- **Weather Correlation Heatmap:** `general/heatmap_for_correlation_weather.py`  
- **Regression: Temperature vs Steps:** `general/plot_linear_regression_weather.py`

---

###  User-Specific Analysis

- **Steps/Distance Charts:** `user_spec/steps_and_distance_user.py`  
- **Calories Burned:** `user_spec/calories_user.py`  
- **Activity Type Proportions:** `user_spec/pie_chart_minutes.py`  
- **Calories vs Steps Regression:** `user_spec/calories_steps_regression.py`  
- **Active vs Sedentary Minutes:** `user_spec/sedentary_versus_tot
