import matplotlib.pyplot as plt


def plot_calories_per_day(df, user_id, start_date=None, end_date=None):
    user_data = df[df['Id'] == user_id]
    if start_date and end_date:
        user_data = user_data[(user_data['ActivityDate'] >= start_date) & (user_data['ActivityDate'] <= end_date)]
    plt.figure(figsize=(10,5))
    plt.plot(user_data['ActivityDate'], user_data['Calories'], marker='o')
    plt.title(f'Calories Burnt Per Day for User {user_id}')
    plt.xlabel('Date')
    plt.ylabel('Calories')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()