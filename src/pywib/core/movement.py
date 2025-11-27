import pandas as pd
import numpy as np

from pywib.utils import (acceleration_traces, velocity_traces, velocity_df, 
                         acceleration_df, jerkiness_df, jerkiness_traces, 
                         _path, validate_dataframe, compute_space_time_diff, 
                         compute_metrics_from_traces, extract_traces_by_session, 
                         auc_ratio_traces, auc_ratio_df)
from pywib.constants import ColumnNames

def velocity(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = False) -> dict[str, list[pd.DataFrame]]:
    """
    Function to calculate velocity for either a single DataFrame or a traces dictionary.

    If `traces` is None, they will be computed from the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'x', 'y', and 'timeStamp' columns.
        traces (dict[str, list[pd.DataFrame]]): Dictionary mapping session IDs to lists of DataFrames.
        per_traces (bool): Whether to compute velocity per trace. If False, compute directly on df.

    Returns:
        dict[str, list[pd.DataFrame]]: Dictionary of traces with computed 'velocity' column.
    """
    if df is None and traces is None:
        raise ValueError("Either 'df' or 'traces' must be provided.")

    if not per_traces:
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
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean ', 'max', and 'min' velocity.
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

    if not per_traces:
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
        df (pd.DataFrame): DataFrame containing interaction data. Optionally already including 'acceleration' column.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean', 'max', and 'min' acceleration.
    """
    if (ColumnNames.ACCELERATION not in df.columns) and (traces is None):
        validate_dataframe(df)
        if ColumnNames.VELOCITY not in df.columns:
            traces = velocity(df, per_traces=True)
        traces = acceleration(None, traces,  per_traces=True)

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

    if not per_traces:
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

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data. Optionally already including 'jerkiness' column.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean', 'max', and 'min' jerkiness.
    """
    if((ColumnNames.JERKINESS not in df.columns) and (traces is None)):
        validate_dataframe(df)
        if(ColumnNames.ACCELERATION not in df.columns):
            if(ColumnNames.VELOCITY not in df.columns):
                traces = velocity(df, per_traces=True)
            traces = acceleration(None, traces, per_traces=True)
        traces = jerkiness(None, traces, per_traces=True)

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


def auc(df: pd.DataFrame, validation: bool = True, computeTraces: bool = True) -> float | dict:
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

    # TODO revisar
    if computeTraces:
        df = df.sort_values(by=ColumnNames.TIME_STAMP)
        traces = extract_traces_by_session(df)
        auc_by_session = {}
        for session_id, session_traces in traces.items():
            session_traces = compute_space_time_diff(session_traces)
            auc_by_session[session_id] = np.mean([np.trapezoid(trace[ColumnNames.Y], trace[ColumnNames.X]) for trace in session_traces])
        return auc_by_session
    else:
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

def auc_ratio(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = True) -> dict:
    """
    Calculate the AUC ratio for the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
        computeTraces (bool): Whether to compute traces by sessionId, by default True. If False, df is assumed to be already segmented by sessionId.
    
    Returns:
        auc_per_session (dict): A dictionary with sessionId as keys and a tuple (auc, auc_ratio) as values. Where the auc is the area under the curve and auc_ratio is the ratio between the AUC and the optimal AUC.
    """

    if df is None and traces is None:
        raise ValueError("Either 'df' or 'traces' must be provided.")

    if not per_traces:
        # Compute directly on the DataFrame (no trace extraction)
        return auc_ratio_df(df)

    # If traces are not provided, extract them from df
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    return auc_ratio_traces(traces)

def auc_ratio_metrics(df: pd.DataFrame = None, computed_auc: dict = None, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    This function computes the mean, max, and min auc ratio for each session on the given dataframe or list of traces.
    The optimal auc is not given in the output, only the auc ratio and auc, since it can be derived from them if needed.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data.
        computed_auc (dict): Precomputed AUC ratios. If None, they will be computed from df or traces.
        traces (dict): A dictionary with keys as (sessionId) and values as lists of DataFrames. If None, traces will be computed from df.
    Returns:
        dict: A dictionary with keys as (sessionId) and values as dictionaries with 'mean_ratio', 'max_ratio', 'min_ratio' for the auc ratio and 'mean', 'max', and 'min' auc.
    """
    if (computed_auc is None):
        if(df is None):
            raise ValueError("Either 'df' or 'traces' must be provided.")
        if (traces is not None):
            computed_auc = auc_ratio(None, traces=traces, per_traces=True)
        else:
            computed_auc = auc_ratio(df)

    for session_id in computed_auc.keys():
        auc_ratios = [trace_metrics['auc_ratio'] for trace_metrics in computed_auc[session_id]]
        auc = [trace_metrics['auc'] for trace_metrics in computed_auc[session_id]]
        computed_auc[session_id] = {
            'mean_ratio': np.mean(auc_ratios) if auc_ratios else 0,
            'max_ratio': np.max(auc_ratios) if auc_ratios else 0,
            'min_ratio': np.min(auc_ratios) if auc_ratios else 0,
            'mean': np.mean(auc) if auc else 0,
            'max': np.max(auc) if auc else 0,
            'min': np.min(auc) if auc else 0,
        }
    return computed_auc
    

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