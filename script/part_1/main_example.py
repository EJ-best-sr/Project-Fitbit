import seaborn as sns
from load_data import load_data
from plot_distance_per_user import plot_distance_per_user
from plot_workout_frequency_by_day import plot_workout_frequency_by_day
from plot_regression_line import plot_regression_line
from plot_calories_per_day import plot_calories_per_day
from count_unique_users import count_unique_users

# set color palette for default settings
sns.set_palette("viridis")

# load the data using load_data function 
data = load_data('daily_acivity.csv')
print(data.head())

# count unique users in the dataframe
print(f"Total number of unique users: {count_unique_users(data)}")

# plot the distance per user 
plot_distance_per_user(data)

# plot the workout frequency by day for users in the database
plot_workout_frequency_by_day(data)

# plot regression line
plot_regression_line(data, user_id=1503960366)

# plot calories burnt
plot_calories_per_day(data, user_id=1503960366, start_date='2016-03-25', end_date='2016-04-05')


