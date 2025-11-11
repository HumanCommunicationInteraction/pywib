import pandas as pd
from ..constants import ColumnNames
from ..utils.validation import validate_dataframe

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

def compute_metrics_from_traces(
    df: pd.DataFrame,
    traces: dict[str, list[pd.DataFrame]] | None,
    column_name: str,
    compute_traces_fn,
    preprocess_fn=None
) -> dict:
    """
    Compute basic statistical metrics (mean, max, min) for a specific column across sessions.

    This function serves as a generic helper for computing metrics such as velocity or acceleration
    over session-based trace data. It can automatically compute traces if they are not provided and
    allows for custom preprocessing (e.g., filtering out zero values).

    Parameters:
        df (pd.DataFrame): 
            A DataFrame containing the necessary data. Must include the specified column 
            or enough information to compute it via `compute_traces_fn`.

        traces (dict[str, list[pd.DataFrame]] | None): 
            Optional dictionary containing session traces. 
            Each key corresponds to a sessionId, and its value is a list of DataFrames 
            representing that session's traces. If None, traces will be computed using 
            `compute_traces_fn(df)`.

        column_name (str): 
            The name of the column from which to compute metrics (e.g., "velocity", "acceleration").

        compute_traces_fn (Callable): 
            A function that, given a DataFrame, computes and returns the corresponding traces dictionary.

        preprocess_fn (Callable | None): 
            Optional function applied to the concatenated column values before computing statistics. 
            Typically used to filter out zero or invalid values.

    Returns:
        dict:
            A dictionary where keys are sessionIds and values are dictionaries containing:
            - 'mean': Mean value.
            - 'max': Maximum value.
            - 'min': Minimum value.
    """
    if (traces is None) and (column_name not in df.columns):
        validate_dataframe(df)
        traces = compute_traces_fn(df, per_traces=True)

    metrics = {}
    for session_id, session_traces in traces.items():
        values = pd.concat([trace[column_name] for trace in session_traces])
        if preprocess_fn:
            values = preprocess_fn(values)
        metrics[session_id] = {
            'mean': values.mean(),
            'max': values.max(),
            'min': values.min()
        }

    return metrics