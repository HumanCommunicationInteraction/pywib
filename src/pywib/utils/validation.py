import pandas as pd
from ..constants import ColumnNames

required_columns = [
    ColumnNames.SESSION_ID, ColumnNames.EVENT_TYPE, ColumnNames.TIME_STAMP, ColumnNames.X, ColumnNames.Y
]

keyboard_columns = [
   ColumnNames.KEY_VALUE_EVENT, ColumnNames.KEY_CODE_EVENT
]

def validate_dataframe(df: pd.DataFrame):

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        
def validate_dataframe_keyboard(df: pd.DataFrame):

    columns_to_check = required_columns + keyboard_columns

    for col in columns_to_check:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")