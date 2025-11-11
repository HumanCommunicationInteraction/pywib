import pandas as pd
import numpy as np
from pywib.constants import ColumnNames
from pywib.utils import compute_space_time_diff, validate_dataframe

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

    if(ColumnNames.VELOCITY not in df.columns):
        df = velocity_df(df)

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

    if(ColumnNames.ACCELERATION not in df.columns):
        df = acceleration_df(df)

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

def _auc(df: pd.DataFrame) -> float:
    """
    Helper function to calculate the Area Under the Curve (AUC) for a single DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
    Returns:
        float: The computed AUC value.
    """
    validate_dataframe(df)

    df = compute_space_time_diff(df)

    # Área bajo la curva real
    area_real = np.trapezoid(df[ColumnNames.Y], df[ColumnNames.X])
    return area_real

def _auc_optimal(df: pd.DataFrame) -> float:
    """
    Helper function to calculate the Area Under the Optimal Curve for a single DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
    Returns:
        float: The computed Area Under the Optimal Curve value.
    """
    df = compute_space_time_diff(df)

    # Área bajo la línea óptima
    x0, y0 = df[ColumnNames.X].iloc[0], df[ColumnNames.Y].iloc[0]
    x1, y1 = df[ColumnNames.X].iloc[-1], df[ColumnNames.Y].iloc[-1]
    x_opt = np.linspace(x0, x1, len(df))
    y_opt = np.linspace(y0, y1, len(df))
    area_optimal = np.trapezoid(y_opt, x_opt)

    return area_optimal

def auc_ratio_df(df: pd.DataFrame) -> dict:
    """
    Calculate AUC, optimal AUC, and AUC ratio for a single DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
    Returns:
        dict: Dictionary with 'auc', 'auc_optimal', and 'auc_ratio'.
    """
    validate_dataframe(df)
    auc_val = _auc(df)
    area_optimal = _auc_optimal(df)
    return {
        "auc": auc_val,
        "auc_ratio": abs(auc_val - area_optimal) / (abs(area_optimal) + 1e-6)
    }

def auc_ratio_traces(traces: dict[str, list[pd.DataFrame]]) -> dict[list[dict]]:
    """
    Calculate AUC ratio metrics for multiple traces grouped by session IDs.

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Mapping of sessionId to list of DataFrames.
    Returns:
        dict[list[dict]]: Mapping of sessionId to list of AUC ratio metrics dictionaries.
    """
    auc_metrics = {}
    for session_id, session_traces in traces.items():
        auc_metrics_per_trace = []
        for i, df in enumerate(session_traces):
            validate_dataframe(df)
            auc_metrics_per_trace.append(auc_ratio_df(df))
        auc_metrics[session_id] = auc_metrics_per_trace
    return auc_metrics

