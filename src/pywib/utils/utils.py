import pandas as pd
from ..constants import ColumnNames

def compute_space_time_diff(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute space and time differences (dx, dy, dt) for the given DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.
    
    Returns:
        pd.DataFrame: DataFrame with additional 'dx', 'dy', and 'dt' columns.
    """
    if(ColumnNames.X not in df.columns or
       ColumnNames.Y not in df.columns or
       ColumnNames.TIME_STAMP not in df.columns or
       ColumnNames.SESSION_ID not in df.columns):
        raise ValueError(f"DataFrame must contain '{ColumnNames.X}', '{ColumnNames.Y}', '{ColumnNames.TIME_STAMP}', and '{ColumnNames.SESSION_ID}' columns.")

    df = df.copy()
    df.sort_values(by=[ColumnNames.TIME_STAMP], inplace=True)
    df[ColumnNames.TIME_STAMP] = pd.to_numeric(df[ColumnNames.TIME_STAMP], errors='coerce')
    df['dt'] = df.groupby([ColumnNames.SESSION_ID])[ColumnNames.TIME_STAMP].diff().fillna(0)
    df['dx'] = df.groupby([ColumnNames.SESSION_ID])[ColumnNames.X].diff().fillna(0)
    df['dy'] = df.groupby([ColumnNames.SESSION_ID])[ColumnNames.Y].diff().fillna(0)
    return df