import streamlit as st
import pandas as pd
import sys, os
import sqlite3
import math

module_dir = '/data' # this should be a directory where daily_acivity.csv is
sys.path.append(module_dir)
db_path = os.path.normpath("data/fitbit_database.db")
weather_data_path = os.path.normpath("data/Chicago 2016-03-12 to 2016-04-12.csv")
weather_data = pd.read_csv(weather_data_path)

# general
from general.load_data import load_data
from general.total_distances import plot_distances
from general.sleep_regression_analysis import perform_regression_analysis
from general.calories_vs_steps import calories_vs_steps_regression
from general.sleep_vs_activity import analyze_sleep_activity
from general.avg_calories_per_step_bins import avg_calories_per_step_bins
from general.investigate_total_distance_days import investigate_total_distance_days
from general.pie_chart_minutes import plot_activity_distribution
from general.calories_4_hour_blocks_general import plot_calories_per_4_hour_block
from general.sleep_4_hour_blocks_general import plot_sleep_per_4_hour_block
from general.steps_4_hour_blocks_general import plot_steps_per_4_hour_block
from general.height_and_weight_metrics import add_height_column
from general.height_and_weight_metrics import replace_missing_values_weight_log
from general.distances_kruskal import test_distances
from general.sedentary_plot_per_day import investigate_sedentary_minutes_days
from general.sedentary_kruskal import test_sedentary
from general.plot_bmi_pie_chart import plot_bmi_pie_chart
from general.plot_weight_activity import plot_weight_vs_activity
from general.plot_fitbit_usage import plot_fitbit_usage_pie
from general.bmi_vs_total_active_minutes import plot_bmi_relationship

# imports for weather
from general.weather_Chicago_charts import plot_precipitation_chart
from general.plot_steps_rainy_or_not import plot_steps_rainy_vs_non_rainy
from general.heatmap_for_correlation_weather import combined_weather_fitbit_heatmap
from general.plot_linear_regression_weather import plot_steps_vs_temperature_regression


# user-spec
from user_spec.heart_rate_and_intensity import plot_health_metrics
from user_spec.sedentary_versus_total_active_minutes_per_user import plot_active_sedentary_minutes_daily
from user_spec.average_steps_records import count_user_total_steps_records
from user_spec.user_comparison import compare_user_to_database_averages
from user_spec.calories_user import plot_calories_burnt
from user_spec.heart_analysis_user import heart_rate_analysis
from user_spec.steps_and_distance_user import plot_steps_and_distance
from user_spec.sedentary_versus_total_active_minutes_per_user import plot_active_sedentary_minutes_daily
from user_spec.calories_steps_regression import plot_regression_line
from user_spec.sedentary_versus_total_active_minutes_per_user import plot_active_sedentary_minutes_daily

# sleep regression
from sleep_vs_activity.sleep_vs_sedentary import calculate_user_statistics_sedentary, calculate_user_statistics_sleep
from sleep_vs_activity.sleep_vs_sedentary import load_and_process_data
from sleep_vs_activity.sleep_vs_sedentary import load_and_process_sleepdata



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
    .stExpander > div > div > div > button:hover {
        color: #1588ed;
        border: #1588ed;
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
    .custom-delta {
        color: black; /* Change to any color you want */
        font-size: 18px !important; 
        margin-top: -20px !important; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    "<h2 style='text-align: center; color: #4A4A4A;'>Fitbit Data Analysis</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a page:",
    ["General Information", "User-Specific Analysis"]
)

# Set page state
if "page" not in st.session_state:
    st.session_state.page = "General"

if "sub_page" not in st.session_state:
    st.session_state.sub_page = "Home"

# Update page state based on selection
if "General" in page:
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

   

# ---------------------------
# Page 1: General Information
# ---------------------------
if st.session_state.page == "General":
    st.title("Fitbit Data Analytics")

    # Sub-page navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Home"):
            st.session_state.sub_page = "Home"
    with col2:
        if st.button("Regression Analysis"):
            st.session_state.sub_page = "Regression Analysis"
    with col3:
        if st.button("Weekday Analysis"):
            st.session_state.sub_page = "Weekday Analysis"
    with col4:
        if st.button("4-Hour Block Analysis"):
            st.session_state.sub_page = "4-Hour Block Analysis"
    with col5:
        if st.button("Weather Analysis"):
            st.session_state.sub_page = "Weather Analysis"

    # Home Sub-page
    if st.session_state.sub_page == "Home":

        # ----------------------
        # calculate sample sizes
        # ----------------------
        query_hr = "SELECT Id FROM daily_activity"
        td_num = pd.read_sql_query(query_hr, conn)['Id'].nunique()
        sl_num = df_sleep['Id'].nunique()
        sed_num = df_sleep_sed['Id'].nunique()
        wei_hei_num = weight_log_df['Id'].nunique()
        steps_num = pd.read_sql_query(query_hr, conn)['Id'].nunique()
        td_info = f"Sample size: {td_num}"
        sl_info = f"A sleep of less than 3 hours in 24 hours is not taken into the average over all available users in the sample (erroneous data). Sample size: {sl_num}"
        sed_info = f"Sample size: {sed_num}"
        wei_info = f"Sample size: {wei_hei_num}"
        hei_info = f"Sample size: {wei_hei_num}"
        bmi_info = f"Sample size: {wei_hei_num}"
        step_info = f"Sample size: {steps_num}"

        sl_min, sl_sd, num = calculate_user_statistics_sleep(df_sleep)
        sed_min, sed_sd, num = calculate_user_statistics_sedentary(df_sleep_sed)

        # --------
        # Metrics
        # --------
        st.header("Overall Statistics")
        col1, col2, col3, col4, col5, col6, col7,col8, col9 = st.columns(9)
        with col1:
            st.metric("Number of Users", f"{data['Id'].nunique()}",
                      help= "Total number of unique users in the database.")
        with col2:
            st.metric("Average Distance", f"{data['TotalDistance'].mean():.2f} km", help=td_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {data['TotalDistance'].std():.2f} km</p>', unsafe_allow_html=True)
        with col3:
            st.metric("Average Steps", f"{data['TotalSteps'].mean():.0f} steps", help=step_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {data['TotalSteps'].std():.0f} steps</p>', unsafe_allow_html=True)
        with col4:
            st.metric("Average Calories", f"{data['Calories'].mean():.0f} kcal", help=td_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {data['Calories'].std():.0f} kcal</p>', unsafe_allow_html=True)
        with col5:
            st.metric("Average Sleep Duration", f"{sl_min} min", help=sl_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sl_sd:.0f} min</p>', unsafe_allow_html=True)
        with col6:
            st.metric("Average Sedentary Minutes", f"{sed_min} min", help=sed_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sed_sd:.0f} min</p>', unsafe_allow_html=True)
        with col7:
            st.metric("Average Weight", f"{weight_log_df['WeightKg'].mean():.1f} kg", help=wei_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {weight_log_df['WeightKg'].std():.1f} kg</p>', unsafe_allow_html=True)
        with col8:
            st.metric("Average Height", f"{weight_log_df['Height'].mean():.2f} m", help=hei_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {weight_log_df['Height'].std():.1f} m</p>', unsafe_allow_html=True)
        with col9:
            st.metric("Average BMI:", f"{weight_log_df['BMI'].mean():.2f} kg/m²", help=bmi_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {weight_log_df['BMI'].std():.1f} kg/m²</p>', unsafe_allow_html=True)


        # Plots
        st.header("Overall Graphical Analysis")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Total Distance per User")
            fig1 = plot_distances(data)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig_bar, fig_box = avg_calories_per_step_bins(db_path)
            # st.plotly_chart(fig_box)
            st.subheader("Average Calories Burned per Total Steps")
            st.plotly_chart(fig_bar)
            # st.subheader("Sleep Duration vs. Weight")
            # fig = plot_sleep_vs_weight(db_path)
            # st.plotly_chart(fig)


        with col3: 
            st.subheader("Weight vs. Calories Burned")
            fig = plot_weight_vs_activity(db_path)
            st.plotly_chart(fig)

            
        
        col10, col20, col30 = st.columns(3)

        with col10:
            st.subheader("Number of Days Using Fitbit")
            fig_usage = plot_fitbit_usage_pie(db_path)
            st.plotly_chart(fig_usage)
        with col20:
            st.subheader("Active Minutes by Intensity")
            fig = plot_activity_distribution(data)
            st.plotly_chart(fig)
        with col30:
            st.subheader("BMI Classification")
            fig_bmi = plot_bmi_pie_chart(db_path)
            st.plotly_chart(fig_bmi)
            

    # Regression Analysis Sub-page
    elif st.session_state.sub_page == "Regression Analysis":
        st.title("Regression Analysis")
        regression_fig, residuals_histogram, qq_fig, info_r2= perform_regression_analysis(df_sleep_sed)
        info_sl_sed = "The sleep records of less than 3 hours in 24 hours are left out. " + info_r2

        st.header('Sedentary Time vs Sleep Time', help=info_sl_sed)
        col4, col5, col6 = st.columns(3)

        with col4:
            st.plotly_chart(regression_fig)
        with col5:
            st.plotly_chart(residuals_histogram)
        with col6:
            st.plotly_chart(qq_fig)

        col1, col2 = st.columns(2)
        with col1:
            fig, info_c_st = calories_vs_steps_regression(db_path)
            st.header("Calories Burned vs Steps", help = info_c_st)
            st.plotly_chart(fig)
        with col2:
            fig, info_sl_act = analyze_sleep_activity(db_path)
            st.header("Sleep Time vs Activity", help= info_sl_act)
            st.plotly_chart(fig)

        col7, col8 = st.columns(2)
        bmi1, bmi2, text1, text2 = plot_bmi_relationship(db_path)

        with col7:
            st.header("Sedentary Minutes vs BMI", help=text1)
            st.plotly_chart(bmi1, use_container_width = True)
        
        with col8:
            st.header("Total Active Minutes vs BMI", help=text2)
            st.plotly_chart(bmi2, use_container_width=True)




    elif st.session_state.sub_page == "Weekday Analysis":
        st.title("Weekday Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Box plot: Total Distance per Day of the Week")
            with st.expander("Test for significant difference in total distance across different days of the week"):
                stat, p_value = test_distances(conn)

                if stat is None:
                    st.warning("No data available for analysis.")
                else:
                    st.info(f"Kruskal-Wallis Test Result:\n\n- Statistic: {stat:.2f}\n- p-value:{p_value:.4f}")

                    if p_value < 0.05:
                        st.success("There is a significant difference in total distance across different days of the week.")
                    else:
                        st.warning("No significant difference found in total distance across different days of the week.")

            fig = investigate_total_distance_days(conn)
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Box plot: Sedentary Activity per Day of the Week") 
            with st.expander("Test for significant difference in Sedentary Minutes across different days of the week "):
                stat, p_value = test_sedentary(conn)

                if stat is None:
                    st.warning("No data available for analysis.")
                else:
                    st.info(f"Kruskal-Wallis Test Result:\n\n- Statistic: {stat:.2f}\n- p-value: {p_value:.4f}")

                    if p_value < 0.05:
                        st.success("There is a significant difference in sedentary minutes across different days of the week.")
                    else:
                        st.warning("No significant difference found in sedentary minutes across different days of the week.")
            fig = investigate_sedentary_minutes_days(conn)
            st.plotly_chart(fig)

    elif st.session_state.sub_page == "4-Hour Block Analysis":
        st.title("4-Hour Block Analysis")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Average Calories Burnt per 4-Hour Block")
            fig = plot_calories_per_4_hour_block()
            st.plotly_chart(fig)
        with col2:
            st.subheader("Average Minutes of Sleep per 4-Hour Block")
            fig = plot_sleep_per_4_hour_block()
            st.plotly_chart(fig)
        with col3:
            st.subheader("Average Steps per 4-Hour Block")
            fig = plot_steps_per_4_hour_block()
            st.plotly_chart(fig)




    elif st.session_state.sub_page == "Weather Analysis":
        st.title("Weather Analysis: Chicago")
        col1,col2 = st.columns(2)
       
        with col1:
            st.subheader("Daily and Cumulative Precipitation")
            chart = plot_precipitation_chart(weather_data)
            st.plotly_chart(chart, use_container_width=True)
            
            
            
        with col2:
            st.subheader("Heatmap for correlation matrix")
            conn = sqlite3.connect(db_path)
            chart = combined_weather_fitbit_heatmap(weather_data, conn)
            st.plotly_chart(chart)

            
        col10, col20 = st.columns(2)

        with col10:
            st.subheader("Box Plot: Total Steps on Rainy vs Non-Rainy Days")
            fig = plot_steps_rainy_vs_non_rainy(db_path, weather_data)
            st.plotly_chart(fig, use_container_width=True)
        with col20:
            fig, r_squared = plot_steps_vs_temperature_regression(db_path, weather_data)

            st.subheader("Linear Regression: Total Steps vs Temperature",
                         help=f"This chart displays a linear regression between daily total steps and recorded temperature.\n\n"
                         f"R-squared value is {r_squared:.5f}. It shows how much variation in step count is explained by temperature.\n\n"
                         f" Interpretation: A higher R² suggests that temperature influences activity. If low, other factors likely play a bigger role.")
            st.plotly_chart(fig, use_container_width=True)
             


    


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

    comparison_result = compare_user_to_database_averages(user_data, data, start_date, end_date)

    weight_log_df['Date'] = pd.to_datetime(weight_log_df['Date'])
    user_weight_log_df = weight_log_df[(weight_log_df['Id'] == selected_user) & 
                                       (weight_log_df['Date'] >= start_date) & (weight_log_df['Date'] <= end_date)]
    weight_data_sorted = user_weight_log_df.sort_values(by='Date', ascending=False)
    if not weight_data_sorted.empty:
        last_bmi = weight_data_sorted.iloc[0]['BMI']
    else:
        user_weight_log_df = weight_log_df[(weight_log_df['Id'] == selected_user)]
        weight_data_sorted = user_weight_log_df.sort_values(by='Date', ascending=False)
        if not weight_data_sorted.empty:
            last_bmi = weight_data_sorted.iloc[0]['BMI']
        else:
            last_bmi = None

    # -------
    # Metrics 
    # -------

    st.subheader("Numerical Summary")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    # ------
    # calculate the sample sizes for the given averages
    # ------
    td_num = user_data['TotalDistance'].count()
    sl_min, sl_sd, sl_num = calculate_user_statistics_sleep(df_sleep, selected_user, start_date, end_date)
    sed_min, sed_sd, sed_num = calculate_user_statistics_sedentary(df_sleep_sed, selected_user, start_date, end_date)
    
    query_steps = "SELECT Id, ActivityDate, TotalSteps FROM daily_activity"
    df_me = pd.read_sql(query_steps, conn)
    df_me['ActivityDate'] = pd.to_datetime(df_me['ActivityDate'])  
    num_records = count_user_total_steps_records(df_me, selected_user)
    
    steps_info = f"Number of records: {num_records}"
    td_info = f"Number of records: {td_num}"
    sl_info = f"Number of records: {sl_num}"
    sed_info = f"Number of records: {sed_num}"

    st.write(comparison_result, unsafe_allow_html=True)

    with col1:
        avg = user_data['TotalDistance'].mean()
        sd = user_data['TotalDistance'].std()
        if math.isnan(avg):
            st.metric("Average Distance", "No data", help=td_info)
        else:
            st.metric("Average Distance", f"{avg:.2f} km", help=td_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sd:.2f} km</p>', unsafe_allow_html=True)
    
    with col2:
        avg_steps = user_data['TotalSteps'].mean()
        st.metric("Average Steps", f"{avg_steps:.0f} steps",  help=steps_info)
        st.markdown(f'<p class="custom-delta">Standard Deviation: {user_data['TotalSteps'].std():.0f} steps</p>', unsafe_allow_html=True)


    with col3:
        avg = user_data['Calories'].mean()
        sd = user_data['Calories'].std()
        if math.isnan(avg):
            st.metric("Average Calories", "No data", help=td_info)
        else:
            st.metric("Average Calories", f"{avg:.0f} kcal", help=td_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sd:.0f} kcal</p>', unsafe_allow_html=True)

    with col4:
        if sl_min is None:
            st.metric("Average Sleep Duration", "No data", help=sl_info)
        else:
            st.metric("Average Sleep Duration", f"{sl_min} min", help=sl_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sl_sd:.0f} min</p>', unsafe_allow_html=True)

    
    with col5:
        if sed_min is None:
            st.metric("Average Sedentary Duration", "No data", help=sl_info)
        else:
            st.metric("Average Sedentary Duration", f"{sed_min} min", help=sl_info)
            st.markdown(f'<p class="custom-delta">Standard Deviation: {sed_sd:.0f} min</p>', unsafe_allow_html=True)

    with col6:
        last_weight = weight_log_df[weight_log_df['Id'] == selected_user]['WeightKg'].iloc[-1] if not weight_log_df[weight_log_df['Id'] == selected_user].empty else None
        if pd.isna(last_weight):
            st.metric("Weight", "No data", help="No weight data available for the selected user.")
        else:
            st.metric("Weight", f"{last_weight:.1f} kg", help="Most recent weight of the selected user.")

    with col7:
        last_height = weight_log_df[weight_log_df['Id'] == selected_user]['Height'].iloc[-1] if not weight_log_df[weight_log_df['Id'] == selected_user].empty else None
        if pd.isna(last_height):
            st.metric("Height", "No data", help="No height data available for the selected user.")
        else:
            st.metric("Height", f"{last_height:.2f} m")

    with col8:
        if last_bmi is None:
            st.metric("BMI", "No data", help="No BMI data available for the selected user.")
        else:
            st.metric("BMI", f"{last_bmi:.2f} kg/m²", help="Last available BMI for the selected user.")

            
    
    
    
    # Plots

    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Total Steps and Total Distance per Day")
        if user_data['TotalDistance'].mean()==0:
            st.warning("No distance data to plot.")
        else:
            fig = plot_steps_and_distance(data, selected_user, start_date, end_date)
            st.plotly_chart(fig)

        st.subheader("Very Active, Fairly Active, and Lightly Active Minutes Proportions")
        fig = plot_activity_distribution(user_data)
        if fig is not None:
            st.plotly_chart(fig)

        st.subheader("Calories vs Steps Regression")
        if (user_data['TotalSteps'].mean() == 0 or user_data['Calories'].mean()==0):
            st.warning("No enough data to perform regression.")
        else:
            fig = plot_regression_line(data, selected_user)
            st.plotly_chart(fig)



    with col2:
        st.subheader("Calories Burnt per Day")
        fig = plot_calories_burnt(data, selected_user, start_date, end_date)
        st.plotly_chart(fig)

        st.subheader("Total Active Minutes versus Sedentary Activity")
        fig = plot_active_sedentary_minutes_daily(conn, selected_user, start_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y"))
        st.plotly_chart(fig)

        st.subheader("Average Heart Rate and Total Intensity per Day")
        fig = plot_health_metrics(conn, selected_user, start_date, end_date)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No heart and intensity data found for this user in the specified date range. Number of users with this data available: 14. Example Id with data available: 2347167796.")
            

        st.subheader(f"Heart rate analysis")

        rmssd_info = "**RMSSD (Root Mean Square of Successive Differences)**: A measure of variability between heartbeats. Higher values indicate better recovery and adaptability."
        sdnn_info = "**SDNN (Standard Deviation of NN intervals)**: Measures overall heart rate variability. Higher values indicate good cardiovascular health."
        pnn50_info = "**PNN50 (Percentage of NN50)**: The percentage of consecutive heartbeats that differ by more than 50 ms. Higher values indicate greater variability."

        query_hr = "SELECT * FROM heart_rate"
        df_hr = pd.read_sql_query(query_hr, conn)
        num_users = df_hr['Id'].nunique()
        
        result = heart_rate_analysis(selected_user)

        if result is not None:
            col1, col2, col3 = st.columns([3, 4, 3])
            col1.metric("RMSSD", f"{result.loc[0, 'User Value']} ms", help=rmssd_info)
            col2.metric("SDNN", f"{result.loc[1, 'User Value']} ms", help=sdnn_info)
            col3.metric("PNN50", f"{result.loc[2, 'User Value']} %", help=pnn50_info)
            st.write("Detailed Metrics:")
            st.dataframe(result)
            st.write(f"*The sample size for the average metric is {num_users}.") 


        else:
            st.warning(f"No heart data found for this user in the specified date range. Number of users with heart data available: {num_users}. Example Id with data available: 2347167796.")

