import matplotlib.pyplot as plt
import seaborn as sb

sb.set_palette("viridis")

def plot_regression_line(df, user_id):
    user_data = df[df['Id'] == user_id]
    plt.figure(figsize=(8, 6))
    sb.regplot(x=user_data['TotalSteps'], y=user_data['Calories'], scatter=True, ci=95, 
               line_kws={'color': (43/255, 129/255, 126/255)},
               scatter_kws={'color': (74/255, 55/255, 111/255)}, 
               )
    plt.xlabel('Total Steps')
    plt.ylabel('Calories')
    plt.title('Total Steps vs Calories Burnt')  
    plt.show()