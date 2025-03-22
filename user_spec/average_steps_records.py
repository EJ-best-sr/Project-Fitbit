import pandas as pd

def count_user_total_steps_records(df_merged, user_id=None, start_date=None, end_date=None):
    if user_id is not None:
        df_filtered = df_merged[df_merged['Id'] == user_id].copy()
    else:
        df_filtered = df_merged.copy()

    df_filtered.loc[:, 'ActivityDate'] = pd.to_datetime(df_filtered['ActivityDate'])  
    if start_date:
        start_date = pd.to_datetime(start_date)
        df_filtered = df_filtered[df_filtered['ActivityDate'] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[df_filtered['ActivityDate'] <= end_date]

    num_records = df_filtered['TotalSteps'].count()

    return num_records
