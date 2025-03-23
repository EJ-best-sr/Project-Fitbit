import pandas as pd
import plotly.express as px
import sqlite3
def plot_steps_rainy_vs_non_rainy(db_path: str, df_weather: pd.DataFrame):
    try:
        conn = sqlite3.connect(db_path)
        df_fitbit = pd.read_sql_query("SELECT ActivityDate AS date, TotalSteps FROM daily_activity", conn)
        df_fitbit["date"] = pd.to_datetime(df_fitbit["date"]).dt.date

        df_weather = df_weather.copy()
        if "datetime" in df_weather.columns:
            df_weather["date"] = pd.to_datetime(df_weather["datetime"]).dt.date
        elif "date" in df_weather.columns:
            df_weather["date"] = pd.to_datetime(df_weather["date"]).dt.date
        else:
            raise ValueError("Weather data must contain either 'datetime' or 'date' column.")

        # Merge and flag rainy days
        df_merged = pd.merge(df_fitbit, df_weather, on="date", how="inner")
        df_merged["Rainy"] = df_merged["precip"] > 0

        # Make sure columns are good
        if "TotalSteps" not in df_merged.columns:
            raise ValueError("Missing 'TotalSteps' in merged DataFrame.")

        fig = px.box(
            df_merged,
            x="Rainy",
            y="TotalSteps",
            labels={"Rainy": "Rainy Day (True/False)", "TotalSteps": "Total Steps"},
            width=800,               
            height=550,  
        )
        return fig
    
    except Exception as e:
        import plotly.graph_objects as go
        return go.Figure().update_layout(
            title=f"Error: {e}",
            template="plotly_white"
        )