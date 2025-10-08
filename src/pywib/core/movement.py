import pandas as pd
import numpy as np
from ..utils.validation import validate_dataframe
from ..utils.utils import compute_space_time_diff
from ..utils.segmentation import extract_traces_by_session
from ..constants import ColumnNames

def velocity(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate the velocity for the given DataFrame or traces.
    This function computes the velocity based on the distance and time difference between consecutive points.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as DataFrames with an additional 'velocity' column.
    """

    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)
            
    for session_id, session_traces in traces.items():
        for i in range(len(session_traces)):
                validate_dataframe(session_traces[i])

        for j in range(len(session_traces)):
            session_traces[j] = _path(session_traces[j])
            session_traces[j]['velocity'] = session_traces[j]['distance'] / session_traces[j]['dt']
            # Fix NaN velocity for first point - set to 0
            session_traces[j]['velocity'] = session_traces[j]['velocity'].fillna(0)
            
        traces[session_id] = session_traces
    return traces

def velocity_metrics(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate velocity metrics for the given DataFrame or traces.
    This function computes the mean, max, and min velocity for each session.
    """
    
    if((ColumnNames.VELOCITY not in df.columns) and (traces is None)):
        validate_dataframe(df)
        traces = velocity(df)

    metrics = {}
    for session_id, session_traces in traces.items():
        all_velocities = pd.concat([trace['velocity'] for trace in session_traces])
        all_velocities = all_velocities[all_velocities > 0]  # Exclude zero velocities for metrics calculation
        metrics[session_id] = {
            'mean': all_velocities.mean(),
            'max': all_velocities.max(),
            'min': all_velocities.min()
        }

    return metrics

def acceleration(df: pd.DataFrame,  traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate the acceleration for the given DataFrame.
    This function computes the acceleration based on the change in velocity over time.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'velocity' and 'dt' columns.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as DataFrames with an additional 'acceleration' column.
    """
    
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    for session_id, session_traces in traces.items():
        for i in range(len(session_traces)):
                validate_dataframe(session_traces[i])
        for j in range(len(session_traces)):
            session_traces[j]['acceleration'] = session_traces[j]["velocity"].diff().fillna(0) / session_traces[j]['dt']
            session_traces[j]['acceleration'] = session_traces[j]['acceleration'].fillna(0)

        traces[session_id] = session_traces
    return traces

def jerkiness(df: pd.DataFrame,  traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate the jerkiness for the given DataFrame.
    This function computes the jerkiness based on the change in acceleration over time.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'acceleration' and 'dt' columns.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.

    Returns:
        dict: A dictionary with keys as (sessionId) and values as DataFrames with an additional 'jerkiness' column.
    """

    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    for session_id, session_traces in traces.items():
        for i in range(len(session_traces)):
                validate_dataframe(session_traces[i])
        for j in range(len(session_traces)):
            session_traces[j] = session_traces[j]["acceleration"].diff().fillna(0) / session_traces[j]['dt']
            session_traces[j]['jerkiness'] = session_traces[j]['jerkiness'].fillna(0)

        traces[session_id] = session_traces

    return traces

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
            df[session_id] = session_traces

    return df

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

