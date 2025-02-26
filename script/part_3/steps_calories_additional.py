import sqlite3
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


sns.set_palette("viridis")
conn = sqlite3.connect('fitbit_database.db')

query_steps = '''
SELECT Id, 
       TotalSteps,
       Calories
FROM daily_activity
'''
df = pd.read_sql_query(query_steps, conn)


df['StepsBins'] = pd.cut(df['TotalSteps'], bins=[0, 1000, 2000, 5000, 7000, 10000, 15000, float('inf')], 
                         labels=['0-1k', '1-2k', '2-5k', '5k-7k', '7k-10k', '10k-15k', '15k+'])

df_grouped = df.groupby('StepsBins')['Calories'].mean().reset_index()

# Bar plot
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='StepsBins', y='Calories', data=df_grouped, palette='viridis')

# bar coords
x_coords = ax.get_xticks()
y_coords = df_grouped['Calories']

# trend line connecting middle points
plt.plot(x_coords, y_coords, marker='o', color='black', linestyle='-', linewidth=2, label='Trend Line')

# Add labels and title
plt.xlabel('Total Steps In a Day')
plt.ylabel('Average Calories Burned')
plt.title('Bar Plot: Average Calories Burned by Total Steps Bins')
plt.legend()
plt.show()

# Box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='StepsBins', y='Calories', data=df, palette="viridis_r")
plt.xlabel('Total Steps Bins')
plt.ylabel('Calories Burned')
plt.title('Box Plot: Calories Burned by Total Steps Bins')
plt.show()

# # Violin plot
# plt.figure(figsize=(10, 6))
# sns.violinplot(x='StepsBins', y='Calories', data=df, palette="viridis_r")
# plt.xlabel('Total Steps Bins')
# plt.ylabel('Calories Burned')
# plt.title('Violin Plot: Calories Burned by Total Steps Bins')
# plt.show()