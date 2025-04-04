import pandas as pd
import streamlit as st

def compare_user_to_database_averages(user_data, data, start_date, end_date):
    """
    Compare the user's average steps, distance traveled, sedentary minutes, and calories burned 
    to the total database averages for the same metrics within a given date range.
    """

    total_data = data[(data['ActivityDate'] >= start_date) & (data['ActivityDate'] <= end_date)]
    
    avg_total_steps = total_data['TotalSteps'].mean()
    avg_total_distance = total_data['TotalDistance'].mean()
    avg_sedentary_minutes = total_data['SedentaryMinutes'].mean()
    avg_calories_burned = total_data['Calories'].mean()

    avg_user_steps = user_data['TotalSteps'].mean()
    avg_user_distance = user_data['TotalDistance'].mean()
    avg_user_sedentary_minutes = user_data['SedentaryMinutes'].mean()
    avg_user_calories = user_data['Calories'].mean()

    def compare_metric(user_avg, total_avg, metric_name):
        if user_avg > total_avg:
            return f"• <b>Average</b> <b>{metric_name}</b> is <b>higher</b> than the database average of <b>{total_avg:.1f}</b>."
        elif user_avg < total_avg:
            return f"• <b>Average</b> <b>{metric_name}</b> is <b>lower</b> than the database average of <b>{total_avg:.1f}</b>."
        else:
            return f"• <b>Average</b> <b>{metric_name}</b> is equal to the database average of <b>{total_avg:.1f}</b>."

    step_message = compare_metric(avg_user_steps, avg_total_steps, "steps")
    distance_message = compare_metric(avg_user_distance, avg_total_distance, "distance")
    sedentary_message = compare_metric(avg_user_sedentary_minutes, avg_sedentary_minutes, "sedentary minutes")
    calories_message = compare_metric(avg_user_calories, avg_calories_burned, "calories burned")

    comparison_message = f"""
    <p style="font-size: 28px;">
    <b>Comparison for this date range:</b><br>

    <span style="font-size: 25px;">{step_message}</span> <br><br>
    <span style="font-size: 25px;">{distance_message}</span> <br><br>
    <span style="font-size: 25px;">{sedentary_message}</span> <br><br>
    <span style="font-size: 25px;">{calories_message}</span> <br><br>
    </p>
    """

    
    return comparison_message

