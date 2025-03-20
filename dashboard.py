import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import sys, os
import sqlite3

module_dir = '/data' # this should be a directory where daily_acivity.csv is
sys.path.append(module_dir)
db_path = os.path.normpath("data/fitbit_database.db")

from general import steps_4_hour_blocks_general
from script.part_1.load_data import load_data
from general.total_distances import plot_distances
from sleep_vs_activity.sleep_vs_sedentary import calculate_user_statistics_sedentary, calculate_user_statistics_sleep
from sleep_vs_activity.sleep_vs_sedentary import load_and_process_data
from sleep_vs_activity.sleep_vs_sedentary import load_and_process_sleepdata
from user_spec.calories_steps_regression import plot_regression_line
from general.plot_workout_frequency_by_day import plot_workout_frequency_by_day
from general.sleep_regression_analysis import perform_regression_analysis
from general.calories_vs_steps import calories_vs_steps_regression
from general.avg_calories_per_step_bins import avg_calories_per_step_bins
from general.investigate_total_distance_days import investigate_total_distance_days
from user_spec.sedentary_versus_total_active_minutes_per_user import plot_active_sedentary_minutes_daily
from general.pie_chart_minutes import plot_activity_distribution
from general.average_steps import calculate_average_steps
from user_spec.calories_user import plot_calories_burnt
from user_spec.heart_analysis_user import heart_rate_analysis
from user_spec.steps_and_distance_user import plot_steps_and_distance
from general.calories_4_hour_blocks_general import plot_calories_per_4_hour_block
from general.sleep_4_hour_blocks_general import plot_sleep_per_4_hour_block
from general.steps_4_hour_blocks_general import plot_steps_per_4_hour_block
from general.height_and_weight_metrics import add_height_column
from general.height_and_weight_metrics import replace_missing_values_weight_log
from general.plot_bmi_distribution import plot_bmi_distribution



st.set_page_config(layout="wide")

# CSS
st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 2px solid black;
        background-color: white;
        color: black;
        padding: 10px 24px;
        cursor: pointer;
        float: left;
    }
    .stButton > button:hover {
    color: #1588ed;
    border: 2px solid #1588ed;
    }
    .stButton > button:active {
    background-color: white;
    color: #1588ed;
    border: 2px solid #1588ed; 
    }
    .stColumns > div {
        flex: 1;
    }
    .stColumns > div:first-child {
        flex: 0.4;  /* Make the first column smaller */
    }
    .stColumns > div:nth-child(2) {
        flex: 2;  /* Make the second column wider */
    }
    .stColumns > div:last-child {
        flex: 2;  /* Make the third column wider */
    }
    .block-container {
        padding-top: 5rem;
    }
    h3 {
        margin-bottom: 0px;
    }
    .element-container {
        padding-top: 0px;
        margin-top: 0px;
    }
    .metric-box {
    padding: 20px;
    background-color: #f0f2f6;
    border-radius: 10px;
    text-align: center;
    position: relative;
    display: inline-block;
    margin: 10px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position above the text */
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def metric_box(metric_value, metric_label, tooltip_text):
    return f"""
    <div class="metric-box">
        {metric_label}<br>
        <b>{metric_value:.2f} km</b>
        <div class="tooltip">(?)
            <span class="tooltiptext">{tooltip_text}</span>
        </div>
    </div>
    """


# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "General"

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "Home"

# Navigation in the sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["General Information", "User-Specific Analysis"])
if page == "General Information":
    st.session_state.page = "General"
else:
    st.session_state.page = "User-Specific"



# Load the dataframes here
data = load_data('data/daily_acivity.csv')
data['ActivityDate'] = pd.to_datetime(data['ActivityDate'])
df_sleep_sed = load_and_process_data(db_path)
df_sleep = load_and_process_sleepdata(db_path)
conn = sqlite3.connect(db_path)
weight_log_df = add_height_column(replace_missing_values_weight_log(db_path))


# Custom CSS for metric boxes
st.markdown(
    """
    <style>
    .metric-box {
        border: 1px solid #0068C9;  /* Border color matches Plotly blue */
        border-radius: 5px;
        padding: 10px;
        background-color: #0068C9;  /* Default Plotly blue for background */
        text-align: center;
        margin: 5px;
        color: white;  /* White text */
        font-weight: bold;
    }
    .metric-box b {
        color: white;  /* White text for bold values */
    }
    </style>     
    """,
    unsafe_allow_html=True,
)    

# ---------------------------
# Page 1: General Information
# ---------------------------
if st.session_state.page == "General":
    st.title("Fitbit Data Analytics")

    # Sub-page navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Home"):
            st.session_state.sub_page = "Home"
    with col2:
        if st.button("Regression Analysis"):
            st.session_state.sub_page = "Regression Analysis"

    # Home Sub-page
    if st.session_state.sub_page == "Home":

        # ----------------------
        # calculate sample sizes
        # ----------------------
        query_hr = "SELECT Id FROM daily_activity"
        td_num = pd.read_sql_query(query_hr, conn)['Id'].nunique()
        sl_num = df_sleep['Id'].nunique()
        sed_num = df_sleep_sed['Id'].nunique()
        td_info = f"Sample size: {td_num}"
        sl_info = f"A sleep of less than 3 hours in 24 hours is not taken into the average over all available users in the sample (erroneous data). Sample size: {sl_num}"
        sed_info = f"Sample size: {sed_num}"

        sl_min, a = calculate_user_statistics_sleep(df_sleep)
        sed_min, b = calculate_user_statistics_sedentary(df_sleep_sed)

        # Metrics
        st.header("Overall Statistics")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            #st.markdown('<div class="metric-box">Total users<br><b>{}</b></div>'.format(data['Id'].nunique()), unsafe_allow_html=True)
            st.metric("Number of Users", f"{data['Id'].nunique()}", help= "Total number of unique users in the database.")
        with col2:
            # st.markdown('<div class="metric-box">Average Distance<br><b>{:.2f} km</b></div>'.format(
            #     data['TotalDistance'].mean()), unsafe_allow_html=True)
            st.metric("Average Distance", f"{data['TotalDistance'].mean():.2f} km", help=td_info)
        with col3:
            # st.markdown('<div class="metric-box">Average Calories<br><b>{:.0f} kcal</b></div>'.format(
            #     data['Calories'].mean()), unsafe_allow_html=True)
            st.metric("Average Calories", f"{data['Calories'].mean():.0f} km", help=td_info)
        with col4:
            # st.markdown('<div class="metric-box">Average Sleep Duration<br><b>{} min</b></div>'.format(
            #     calculate_user_statistics_sleep(df_sleep)), unsafe_allow_html=True)
            st.metric("Average Sleep Duration", f"{sl_min} min", help=sl_info)
        with col5:
            # st.markdown('<div class="metric-box">Average Sedentary Minutes<br><b>{} min</b></div>'.format(
            #     calculate_user_statistics_sedentary(df_sleep_sed)), unsafe_allow_html=True)
            st.metric("Average Sedentary Minutes", f"{sed_min} min", help=sed_info)
        with col6:
            st.markdown('<div class="metric-box">Average Weight<br><b>{:.1f} kg</b></div>'.format(
                weight_log_df['WeightKg'].mean()), unsafe_allow_html=True)
        with col7:
            st.markdown('<div class="metric-box">Average Height<br><b>{:.2f} m</b></div>'.format(
                weight_log_df['Height'].mean()), unsafe_allow_html=True)
            

        # Plots
        st.header("Overall Graphical Analysis")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Total Distance per User")
            fig1 = plot_distances(data)
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Average Calories Burned per Total Steps")
            fig_bar, fig_box = avg_calories_per_step_bins(db_path)
            st.plotly_chart(fig_bar)

            st.subheader("Average Calories Burnt per 4-Hour Block")
            fig = plot_calories_per_4_hour_block()
            st.plotly_chart(fig)

        with col2:
            st.subheader("Workout Frequency by Day")
            fig = plot_workout_frequency_by_day(data)
            st.plotly_chart(fig)
        
            st.subheader("Average Calories Burned per Total Steps: Box Plot")
            st.plotly_chart(fig_box)

            st.subheader("Average Minutes of Sleep per 4-Hour Block")
            fig = plot_sleep_per_4_hour_block()
            st.plotly_chart(fig)


        with col3: 
            st.subheader("Box plot: Total Distance per Day of the Week")
            fig = investigate_total_distance_days(conn)
            st.plotly_chart(fig)

            st.subheader("BMI Distribution")
            fig = plot_bmi_distribution(db_path)
            st.plotly_chart(fig)

            st.subheader("Average Steps per 4-Hour Block")
            fig = plot_steps_per_4_hour_block()
            st.plotly_chart(fig)


        st.subheader("Sample Data")
        st.dataframe(data.head())

    # Regression Analysis Sub-page
    elif st.session_state.sub_page == "Regression Analysis":
        st.title("Regression Analysis")

        st.header('Sedentary Time vs Sleep Time Analysis')
        col4, col5, col6 = st.columns(3)

        regression_fig, residuals_histogram, qq_fig = perform_regression_analysis(df_sleep_sed)

        with col4:
            st.plotly_chart(regression_fig)
        with col5:
            st.plotly_chart(residuals_histogram)
        with col6:
            st.plotly_chart(qq_fig)

        st.header("Calories Burned vs Steps")
        st.subheader("Calories Burned vs Steps")
        fig = calories_vs_steps_regression(db_path)
        st.plotly_chart(fig)


#---------------------------
# Page 2: User-Specific Analysis
# ---------------------------
elif st.session_state.page == "User-Specific":
    
    # User selection
    st.sidebar.header("User Selection")
    unique_users = data['Id'].unique().tolist()
    selected_user = st.sidebar.selectbox("Select a User", unique_users)
    # Date selection
    st.sidebar.header("Date Range Selection")
    min_date = data['ActivityDate'].min().to_pydatetime()
    max_date = data['ActivityDate'].max().to_pydatetime()
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    user_data = data[(data['Id'] == selected_user) & (data['ActivityDate'] >= start_date) & (data['ActivityDate'] <= end_date)]
    
    st.title(f"Analysis for User: {selected_user}")
    st.write(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    # Metrics (numerical summary)
    st.subheader("Numerical Summary")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    # ------
    # calculate the sample sizes for the given averages
    # ------
    td_num = user_data['TotalDistance'].count()
    sl_min, sl_num = calculate_user_statistics_sleep(df_sleep, selected_user, start_date, end_date)
    sed_min, sed_num = calculate_user_statistics_sedentary(df_sleep_sed, selected_user, start_date, end_date)

    td_info = f"Number of records: {td_num}"
    sl_info = f"Number of records: {sl_num}"
    sed_info = f"Number of records: {sed_num}"

    with col1:
        # st.markdown('<div class="metric-box">Average Distance<br><b>{:.2f} km</b></div>'.format(
        #     user_data['TotalDistance'].mean()), unsafe_allow_html=True, help=td_info)
        # st.markdown(metric_box(user_data['TotalDistance'].mean(), "Average Distance", td_info), unsafe_allow_html=True)
        st.metric("Average Distance", f"{user_data['TotalDistance'].mean():.2f} km", help=td_info)
    with col2:
        # st.markdown('<div class="metric-box">Average Calories<br><b>{:.0f} kcal</b></div>'.format(
        #     user_data['Calories'].mean()), unsafe_allow_html=True)
        st.metric("Average Calories", f"{user_data['Calories'].mean():.0f} km", help=td_info)
    with col3:
        # st.markdown('<div class="metric-box">Average Sleep Duration<br><b>{} min</b></div>'.format(
        #     calculate_user_statistics_sleep(df_sleep, selected_user, start_date, end_date)), unsafe_allow_html=True)
        st.metric("Average Sleep Duration", f"{sl_min} min", help=sl_info)
    with col4:
        # st.markdown('<div class="metric-box">Average Sedentary Minutes<br><b>{} min</b></div>'.format(
        #     calculate_user_statistics_sedentary(df_sleep_sed, selected_user, start_date, end_date)), unsafe_allow_html=True)
        st.metric("Average Sedentary Minutes", f"{sed_min} min", help=sed_info)

    with col5:
        if pd.isna(weight_log_df[weight_log_df.index == selected_user]['WeightKg'].mean()):
            st.markdown('<div class="metric-box" style="color:red;">No Weight data</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-box">Average Weight<br><b>{:.1f} kg</b></div>'.format(weight_log_df[weight_log_df.index == selected_user]['WeightKg'].mean()), unsafe_allow_html=True)
    with col6:
        if pd.isna(weight_log_df[weight_log_df.index == selected_user]['Height'].mean()):
            st.markdown('<div class="metric-box" style="color:red;">No Height data</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-box">Average Height<br><b>{:.2f} m</b></div>'.format(weight_log_df[weight_log_df.index == selected_user]['Height'].mean()), unsafe_allow_html=True)
    

    # Plots

    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Total Steps and Total Distance per Day")
        fig = plot_steps_and_distance(data, selected_user, start_date, end_date)
        st.plotly_chart(fig)

        st.subheader("Calories vs Steps Regression")
        fig = plot_regression_line(data, selected_user)
        st.plotly_chart(fig)


    with col2:
        st.subheader("Calories Burnt per Day")
        fig = plot_calories_burnt(data, selected_user, start_date, end_date)
        st.plotly_chart(fig)
    
        rmssd_info = "**RMSSD (Root Mean Square of Successive Differences)**: A measure of variability between heartbeats. Higher values indicate better recovery and adaptability."
        sdnn_info = "**SDNN (Standard Deviation of NN intervals)**: Measures overall heart rate variability. Higher values indicate good cardiovascular health."
        pnn50_info = "**PNN50 (Percentage of NN50)**: The percentage of consecutive heartbeats that differ by more than 50 ms. Higher values indicate greater variability."

        result = heart_rate_analysis(selected_user)
        if result is not None:
            st.subheader(f"Heart rate analysis")
            col1, col2, col3 = st.columns([3, 4, 3])
            col1.metric("RMSSD", f"{result.loc[0, 'User Value']} ms", help=rmssd_info)
            col2.metric("SDNN", f"{result.loc[1, 'User Value']} ms", help=sdnn_info)
            col3.metric("PNN50", f"{result.loc[2, 'User Value']} %", help=pnn50_info)
            st.write("Detailed Metrics:")
            st.dataframe(result)

        else:
            st.write("No heart data found for this user.")
            query_hr = "SELECT * FROM heart_rate"
            df_hr = pd.read_sql_query(query_hr, conn)
            num_users = df_hr['Id'].nunique()
            st.write(f"Number of users with heart data available: {num_users}")

    st.dataframe(df_sleep.head())


