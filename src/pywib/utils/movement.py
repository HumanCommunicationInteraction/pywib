import pandas as pd
from pywib.utils.validation import validate_dataframe

def velocity_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate velocity for a single DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.

    Returns:
        pd.DataFrame: DataFrame with an additional 'velocity' column.
    """
    validate_dataframe(df)
    df = _path(df)  # Compute distance and dt first
    df['velocity'] = df['distance'] / df['dt']
    df['velocity'] = df['velocity'].fillna(0)  # Replace NaN (first point) with 0
    return df


def velocity_traces(traces: dict[str, list[pd.DataFrame]]) -> dict[str, list[pd.DataFrame]]:
    """
    Calculate velocity for a dictionary of traces (each a list of DataFrames).

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Mapping of sessionId to list of DataFrames.

    Returns:
        dict[str, list[pd.DataFrame]]: Same structure, but with velocity computed in each DataFrame.
    """
    for session_id, session_traces in traces.items():
        for i, df in enumerate(session_traces):
            validate_dataframe(df)
            session_traces[i] = velocity_df(df)
        traces[session_id] = session_traces
    return traces

import pandas as pd

def acceleration_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate acceleration for a single DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.

    Returns:
        pd.DataFrame: DataFrame with an additional 'acceleration' column.
    """
    validate_dataframe(df)
    df['acceleration'] = df['velocity'].diff().fillna(0) / df['dt']
    df['acceleration'] = df['acceleration'].fillna(0)
    return df


def acceleration_traces(traces: dict[str, list[pd.DataFrame]]) -> dict[str, list[pd.DataFrame]]:
    """
    Calculate acceleration for a dictionary of traces (each a list of DataFrames).

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Mapping of sessionId to list of DataFrames.

    Returns:
        dict[str, list[pd.DataFrame]]: Same structure, but with acceleration computed in each DataFrame.
    """
    for session_id, session_traces in traces.items():
        for i, df in enumerate(session_traces):
            validate_dataframe(df)
            session_traces[i] = acceleration_df(df)
        traces[session_id] = session_traces
    return traces

def jerkiness_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate jerkiness for a single DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.

    Returns:
        pd.DataFrame: DataFrame with an additional 'jerkiness' column.
    """
    validate_dataframe(df)
    df['jerkiness'] = df['acceleration'].diff().fillna(0) / df['dt']
    df['jerkiness'] = df['jerkiness'].fillna(0)
    return df


def jerkiness_traces(traces: dict[str, list[pd.DataFrame]]) -> dict[str, list[pd.DataFrame]]:
    """
    Calculate jerkiness for a dictionary of traces (each a list of DataFrames).

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Mapping of sessionId to list of DataFrames.

    Returns:
        dict[str, list[pd.DataFrame]]: Same structure, but with jerkiness computed in each DataFrame.
    """
    for session_id, session_traces in traces.items():
        for i, df in enumerate(session_traces):
            validate_dataframe(df)
            session_traces[i] = jerkiness_df(df)
        traces[session_id] = session_traces
    return traces


def jerkiness(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None) -> dict[str, list[pd.DataFrame]]:
    """
    Compute jerkiness for either a single DataFrame or multiple traces.

    If `traces` is not provided, they are extracted from `df` using `extract_traces_by_session()`.

    Parameters
    ----------
    df : pd.DataFrame, optional
        DataFrame containing 'acceleration' and 'dt' columns.
    traces : dict[str, list[pd.DataFrame]], optional
        Dictionary mapping session IDs to lists of DataFrames.

    Returns
    -------
    dict[str, list[pd.DataFrame]]
        Dictionary of traces, each containing the computed 'jerkiness' column.
    """
    if traces is None:
        if df is None:
            raise ValueError("Either 'df' or 'traces' must be provided.")
        validate_dataframe(df)
        traces = extract_traces_by_session(df)
    return jerkiness_traces(traces)

def _path(trace: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to calculate the path length for a single trace.
    This function computes the path length based on the Euclidean distance between consecutive points.

    Parameters:
        trace (pd.DataFrame): A single trace DataFrame.

    Returns:
        pd.DataFrame: DataFrame with an additional 'distance' column representing the path length.
    """

    if trace is None:
        raise ValueError("Trace DataFrame must be provided.")

    validate_dataframe(trace)

    trace = compute_space_time_diff(trace)
    trace['distance'] = np.sqrt(trace['dx'] ** 2 + trace['dy'] ** 2)

    return trace
