import pandas as pd
from ..constants import ColumnNames

required_columns = [
    ColumnNames.SESSION_ID, ColumnNames.EVENT_TYPE, ColumnNames.TIME_STAMP, ColumnNames.X, ColumnNames.Y
]

keyboard_columns = [
   ColumnNames.KEY_VALUE_EVENT, ColumnNames.KEY_CODE_EVENT
]

def validate_dataframe(df: pd.DataFrame, except_duplicate_timestamps: bool = False):

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        
    # Ensure no duplicate timestamps per session
    for session_id, group in df.groupby(ColumnNames.SESSION_ID):
        if group[ColumnNames.TIME_STAMP].duplicated().any():
            if except_duplicate_timestamps:
                raise ValueError(f"Duplicate timestamps found in session {session_id}")
            else:
                print(f"Warning: Duplicate timestamps found in session {session_id}")
        
def validate_dataframe_keyboard(df: pd.DataFrame):

    validate_dataframe(df)

    columns_to_check = keyboard_columns

    for col in columns_to_check:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")