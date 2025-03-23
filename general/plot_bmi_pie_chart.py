import sqlite3
import pandas as pd
import plotly.graph_objects as go

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

    bmi_counts = bmi_data["BMI_Category"].value_counts().reset_index()
    bmi_counts.columns = ["BMI Category", "Count"]

    labels = bmi_counts["BMI Category"].tolist()
    values = bmi_counts["Count"].tolist()
    colors = [
    'rgba(147, 112, 219, 0.8)',  # mediumpurple with 60% opacity
    'rgba(106, 90, 205, 0.9)',   # slateblue with 80% opacity
    'rgba(72, 61, 139, 1.0)',    # darkslateblue with 100% opacity
    'rgba(216, 191, 216, 0.7)'   # thistle with 70% opacity
]

    font_sizes = [40 if label == "Normal Weight" else 16 for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hoverinfo="label+percent",
        textinfo="percent",
        insidetextorientation="horizontal",
        textfont=dict(color="white", size=font_sizes),
        marker=dict(colors=colors)
    )])

    fig.update_layout(
        showlegend=True,
        template='plotly_white',
        width=800,
        height=400,
        margin=dict(l=0, r=50, t=50, b=0),
        legend=dict(
            title="BMI Categories",
            font=dict(size=14),
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='black',
            borderwidth=1,
            x=0.80,
            y=0.80,
        )
    )

    return fig