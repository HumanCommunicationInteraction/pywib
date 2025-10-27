import pandas as pd
import numpy as np

from pywib.utils.movement import acceleration_traces, jerkiness_traces, velocity_traces, velocity_df, acceleration_df, jerkiness_df, jerkiness_traces
from pywib.utils.validation import validate_dataframe
from pywib.utils.utils import compute_space_time_diff, compute_metrics_from_traces
from pywib.utils.segmentation import extract_traces_by_session
from pywib.constants import ColumnNames

def velocity(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = False) -> dict[str, list[pd.DataFrame]]:
    """
    Wrapper function to calculate velocity for either a single DataFrame or a traces dictionary.

    If `traces` is None, they will be computed from the DataFrame.
    """
    if df is None and traces is None:
        raise ValueError("Either 'df' or 'traces' must be provided.")

    if per_traces:
        # Compute directly on the DataFrame (no trace extraction)
        return velocity_df(df)

    # If traces are not provided, extract them from df
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    # Compute velocity for each trace
    return velocity_traces(traces)


def velocity_metrics(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate velocity metrics for the given DataFrame or traces.
    This function computes the mean, max, and min velocity for each session.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'velocity' column.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.

    Returns:
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean
    """
    
    return compute_metrics_from_traces(
        df=df,
        traces=traces,
        column_name=ColumnNames.VELOCITY,
        compute_traces_fn=velocity,
        preprocess_fn=lambda s: s[s > 0]  # Exclude zero velocities
    )

def acceleration(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = False) -> dict[str, list[pd.DataFrame]]:
    """
    Wrapper function to calculate acceleration for either a single DataFrame or a traces dictionary.

    If `traces` is None, they will be computed from the DataFrame.
    """
    if df is None and traces is None:
        raise ValueError("Either 'df' or 'traces' must be provided.")

    if per_traces:
        # Compute directly on the DataFrame (no trace extraction)
        return acceleration_df(df)

    # If traces are not provided, extract them from df
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    # Compute acceleration for each trace
    return acceleration_traces(traces)

def acceleration_metrics(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate acceleration metrics for the given DataFrame or traces.
    This function computes the mean, max, and min acceleration for each session.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'acceleration' column.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean', 'max', and 'min' acceleration.
    """
    if (ColumnNames.ACCELERATION not in df.columns) and (traces is None):
        validate_dataframe(df)
        if ColumnNames.VELOCITY not in df.columns:
            traces = velocity(df)
        traces = acceleration(None, traces)

    return compute_metrics_from_traces(
        df=df,
        traces=traces,
        column_name=ColumnNames.ACCELERATION,
        compute_traces_fn=lambda _: traces,  # Already computed above
        preprocess_fn=lambda s: s[s != 0]    # Exclude zero accelerations
    )

def jerkiness(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = False) -> dict[str, list[pd.DataFrame]]:
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
    if df is None and traces is None:
        raise ValueError("Either 'df' or 'traces' must be provided.")

    if per_traces:
        # Compute directly on the DataFrame (no trace extraction)
        return jerkiness_df(df)

    # If traces are not provided, extract them from df
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    # Compute jerkiness for each trace
    return jerkiness_traces(traces)

def jerkiness_metrics(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate jerkiness metrics for the given DataFrame or traces.
    This function computes the mean, max, and min jerkiness for each session.
    """
    if((ColumnNames.JERKINESS not in df.columns) and (traces is None)):
        validate_dataframe(df)
        if(ColumnNames.ACCELERATION not in df.columns):
            if(ColumnNames.VELOCITY not in df.columns):
                traces = velocity(df)
            traces = acceleration(None, traces)
        traces = jerkiness(None, traces)

    return compute_metrics_from_traces(
        df=df,
        traces=traces,
        column_name=ColumnNames.JERKINESS,
        compute_traces_fn=lambda _: traces,  # Already computed above
        preprocess_fn=lambda s: s[s != 0]    # Exclude zero jerkiness
    )

def path(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None) -> pd.DataFrame:
    """
    Calculate the path length for the given DataFrame.
    This function computes the path length based on the Euclidean distance between consecutive points.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.

    Returns:
        pd.DataFrame: DataFrame with an additional 'distance' column representing the path length.
    """

    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    for session_id, session_traces in traces.items():
            for i in range(len(session_traces)):
                validate_dataframe(session_traces[i])

            # Compute the distance for each trace
            for j in range(len(session_traces)):
                session_traces[j]['distance'] = _path(session_traces[j])['distance']
            
            # Store the traces with distance in the dictionary
            traces[session_id] = session_traces

    return traces

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

def auc(df: pd.DataFrame, validation: bool = True, computeTraces: bool = True) -> float:
    """
    Calculate the Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
        validation (bool): Whether to validate the DataFrame structure, by default True.
        computeTraces (bool): Whether to compute traces by sessionId, by default True.
    
    Returns:
        float: The computed AUC value.
    """
    
    if(validation):
        validate_dataframe(df)

    if computeTraces:
        df   = extract_traces_by_session(df)

    df = df.sort_values(by=ColumnNames.TIME_STAMP)

    df = compute_space_time_diff(df)

    # Área bajo la curva real
    area_real = np.trapezoid(df[ColumnNames.Y], df[ColumnNames.X])

    return area_real

def auc_optimal(df: pd.DataFrame, validation: bool = True, computeTraces: bool = True) -> float:
    """
    Calculate the Optimal Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    validation (bool): Whether to validate the DataFrame structure, by default True.
    computeTraces (bool): Whether to compute traces by sessionId, by default True.
    
    Returns:
    float: The computed optimal AUC value.
    """
    
    if(validation):
        validate_dataframe(df)

    if computeTraces:
        df = extract_traces_by_session(df)


    df = compute_space_time_diff(df)

    # Área bajo la línea óptima
    x0, y0 = df[ColumnNames.X].iloc[0], df[ColumnNames.Y].iloc[0]
    x1, y1 = df[ColumnNames.X].iloc[-1], df[ColumnNames.Y].iloc[-1]
    x_opt = np.linspace(x0, x1, len(df))
    y_opt = np.linspace(y0, y1, len(df))
    area_optimal = np.trapezoid(y_opt, x_opt)

    return area_optimal

def auc_ratio(df: pd.DataFrame, computeTraces: bool = True) -> dict:
    """
    Calculate the AUC ratio for the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
        computeTraces (bool): Whether to compute traces by sessionId, by default True. If False, df is assumed to be already segmented by sessionId.
    
    Returns:
        auc_per_session (dict): A dictionary with sessionId as keys and a tuple (area_real, area_optimal, auc_ratio) as values.
    """

    validate_dataframe(df)

    if computeTraces:
        df = extract_traces_by_session(df)

    auc_per_session = {}
    for session_id, session_traces in df.items():
        area_real = auc(session_traces, False, False)
        area_optimal = auc_optimal(session_traces, False, False)
        auc_per_session[session_id] = (area_real, area_optimal, abs(area_real - area_optimal) / (abs(area_optimal) + 1e-6))

    return auc_per_session

def MAD(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate the Mean Absolute Deviation (MAD) for the given DataFrame.
    """
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    metrics = {}
    for session_id, session_traces in traces.items():
        session_mad = []
        session_mad_max = []
        for trace in session_traces:
            session_mad.append(np.mean(np.abs(trace[ColumnNames.Y] - trace[ColumnNames.Y].mean())))
            session_mad_max.append(np.max(np.abs(trace[ColumnNames.Y] - trace[ColumnNames.Y].mean())))
        metrics[session_id] = {
            'mad': np.mean(session_mad) if session_mad else 0,
            'mad_max': np.mean(session_mad_max) if session_mad_max else 0
        }

    return metrics