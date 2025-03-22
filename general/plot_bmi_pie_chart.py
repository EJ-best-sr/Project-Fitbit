import sqlite3
import pandas as pd
import plotly.express as px

def plot_bmi_pie_chart(db_path):
    # Connect and fetch BMI values
    conn = sqlite3.connect(db_path)
    query = "SELECT BMI FROM weight_log"
    bmi_data = pd.read_sql_query(query, conn)
    conn.close()

    # Categorize BMI
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal Weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    bmi_data.dropna(inplace=True)
    bmi_data["BMI_Category"] = bmi_data["BMI"].apply(categorize_bmi)

    # Count categories
    bmi_counts = bmi_data["BMI_Category"].value_counts().reset_index()
    bmi_counts.columns = ["BMI Category", "Count"]

    # Create pie chart
    fig = px.pie(
        bmi_counts,
        values="Count",
        names="BMI Category",
        color_discrete_sequence=px.colors.qualitative.Pastel  # Nice soft palette
    )

    
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        template='plotly_white',
        width=800,  
        height=400,  
        margin=dict(l=0, r=50, t=50, b=0), 
        legend=dict(
            title="Usage Groups",
            font=dict(size=14),         
            bgcolor='rgba(255, 255, 255, 0.5)',  
            bordercolor='black',          
            borderwidth=1,               
            x=0.80,                        
            y=0.80,                       
        ) 
    )
    return fig