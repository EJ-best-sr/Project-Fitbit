import requests
import pandas as pd
import io

# Acquire weather data

# 1st way: Query the VisualCrossing API
def get_weather_data():
    """
    Fetches weather data from VisualCrossing and returns it as a DataFrame.
    """
    weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/retrievebulkdataset?&key=UAPRHZSPNL5S427FH5TZP2Y95&taskId=c6de6002213b5160459955de98041ee2&zip=false"
    response = requests.get(weather_url)
    df = pd.read_csv(io.StringIO(response.text))
    return df

# 2nd way: download a csv from web, then read.
def get_csv_weather_data(csv_path="Chicago 2016-03-25 to 2016-04-12.csv"):
    """
    Reads weather data from a local CSV file.
    """
    df_csv = pd.read_csv(csv_path)
    return df_csv

