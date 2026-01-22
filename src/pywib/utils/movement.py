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
    Calculate AUC and AUC ratio for a single DataFrame, returning them as a dictionary.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
    Returns:
        dict: Dictionary with 'auc', and 'auc_ratio'.
    """
    validate_dataframe(df)
    auc_val = _auc(df)
    area_optimal = _auc_optimal(df)
    df_opt = compute_optimal_path(df)
    # Prepare arrays
    user_x, user_y = df['x'].values, df['y'].values
    opt_x, opt_y = df_opt['x'].values, df_opt['y'].values

    # Compute perpendicular distances from optimal points to user segments
    dists = []
    for i in range(len(opt_x)):
        px, py = opt_x[i], opt_y[i]
        # Compute distance to all user segments and take minimum
        seg_dists = [
            point_to_segment_distance(px, py, user_x[j], user_y[j], user_x[j+1], user_y[j+1])
            for j in range(len(user_x)-1)
        ]
        dists.append(min(seg_dists))

    # Integrate along optimal path
    # Compute optimal path length increments (arc-length)
    dx = np.diff(opt_x)
    dy = np.diff(opt_y)
    ds = np.hypot(dx, dy)
    s_grid = np.concatenate(([0], np.cumsum(ds)))

    auc_perp = np.trapezoid(dists, s_grid)
    
    # Optional normalization by total optimal path length TODO correct?
    total_opt_length = s_grid[-1]
    if total_opt_length > 0:
        auc_perp /= total_opt_length

    return {
        "auc": auc_val,
        "auc_ratio": abs(auc_val - area_optimal) / (abs(area_optimal) + 1e-6),
        'auc_perp': auc_perp
    }

def compute_optimal_path(df: pd.DataFrame, n_points: int = 100) -> pd.DataFrame:
    """
    Compute an "optimal" trajectory as a straight line between start and end points
    of the user path, sampled uniformly with n_points.

    Parameters:
        df (pd.DataFrame): User trajectory with 'x' and 'y' columns.
        n_points (int): Number of points in the optimal path.

    Returns:
        pd.DataFrame: DataFrame with columns 'x' and 'y' representing the optimal path.
    """
    start_x, start_y = df['x'].iloc[0], df['y'].iloc[0]
    end_x, end_y = df['x'].iloc[-1], df['y'].iloc[-1]

    x_opt = np.linspace(start_x, end_x, n_points)
    y_opt = np.linspace(start_y, end_y, n_points)

    df_opt = pd.DataFrame({'x': x_opt, 'y': y_opt})
    return df_opt

def point_to_segment_distance(px, py, x1, y1, x2, y2):
        """Compute the shortest distance from point (px,py) to segment [(x1,y1),(x2,y2)]"""
        # Vector from x1,y1 to px,py
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            # Segment is a point
            return np.hypot(px - x1, py - y1)
        # Project point onto segment, computing parameter t
        t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
        t = np.clip(t, 0, 1)
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        return np.hypot(px - closest_x, py - closest_y)

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

