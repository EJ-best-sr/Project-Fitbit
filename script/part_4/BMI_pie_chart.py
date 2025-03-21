import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
conn = sqlite3.connect("fitbit_database.db")

query = "SELECT BMI FROM weight_log"
bmi_data = pd.read_sql_query(query, conn)

conn.close()

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

bmi_data["BMI_Category"] = bmi_data["BMI"].apply(categorize_bmi)

bmi_category_counts = bmi_data["BMI_Category"].value_counts().reset_index()
bmi_category_counts.columns = ["BMI Category", "Count"]

plt.figure(figsize=(8, 8))
sns.set_palette("viridis")  

plt.pie(bmi_category_counts["Count"], labels=bmi_category_counts["BMI Category"], 
        autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))

plt.title("BMI Distribution of Fitbit Users")
plt.show()