import sqlite3
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os


sns.set_palette("viridis")

# Create the ss1 folder if it doesn't exist
output_folder = 'sc1'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Connect to the SQLite database
conn = sqlite3.connect('fitbit_database.db')

query_steps = '''
SELECT Id,
       ActivityDate, 
       TotalSteps,
       Calories
FROM daily_activity
'''
df_steps = pd.read_sql_query(query_steps, conn)

# Convert ActivityDate to datetime and extract the date
df_steps['ActivityDate'] = pd.to_datetime(df_steps['ActivityDate']).dt.date


# Perform regression analysis on merged data
# Prepare the data for regression
X = df_steps['TotalSteps']  # Independent variable (total active minutes on day 1)
y = df_steps['Calories']  # Dependent variable (total sleep duration from evening of day 1 to morning of day 2)

# Add a constant to the independent variable
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())

# Save regression results to a text file in the try6 folder
with open("sc1/regression_results.txt", "w") as f:
    f.write(model.summary().as_text())

# Visualize the regression results
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_steps['TotalSteps'], y=df_steps['Calories'], alpha=0.9)
sns.regplot(x=df_steps['TotalSteps'], y=df_steps['Calories'], scatter=False, color=(44/255, 131/255, 127/255))
plt.xlabel('Total Steps In A Day')
plt.ylabel('Calories Burnt')
plt.title('Regression: Steps vs Calories')
plt.show()


conn.close()