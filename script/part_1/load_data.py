def load_data(file_path):
    df = pd.read_csv(file_path)
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y')
    return df