import pandas as pd

required_columns = [
    "id", "eventType", "timeStamp", "x", "y"
]

keyboard_columns = [
   "keyValueEvent", "keyCodeEvent"
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