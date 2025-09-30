import pandas as pd

def compute_space_time_diff(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.sort_values(by=['timeStamp'], inplace=True)
    df['timeStamp'] = pd.to_numeric(df['timeStamp'], errors='coerce')
    df['dt'] = df.groupby(['sessionId', 'sceneId'])['timeStamp'].diff().fillna(0)
    df['dx'] = df.groupby(['sessionId', 'sceneId'])['x'].diff().fillna(0)
    df['dy'] = df.groupby(['sessionId', 'sceneId'])['y'].diff().fillna(0)
    return df