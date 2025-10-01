import pandas as pd
import numpy as np
from ..utils.validation import validate_dataframe
from ..utils.utils import compute_space_time_diff
from ..utils.segmentation import extract_traces_by_session

def velocity(df: pd.DataFrame):
    
    # TODO Segmentar en trazas

    validate_dataframe(df)

    df = compute_space_time_diff(df)

    df['velocity'] = df['distance'] / df['dt']
    
    return df

def acceleration(df: pd.DataFrame) -> pd.DataFrame:

    # TODO Segmentar en trazas

    validate_dataframe(df)

    df = compute_space_time_diff(df)
    
    df['acceleration'] = df.groupby(['sessionId', 'sceneId'])['velocity'].diff().fillna(0) / df['dt']

    return df

def path(df: pd.DataFrame) -> pd.DataFrame:

    # TODO Segmentar en trazas

    validate_dataframe(df)
    
    df = compute_space_time_diff(df)

    df['distance'] = np.sqrt(df['dx'] ** 2 + df['dy'] ** 2)

    return df


def auc(df: pd.DataFrame, validation: bool = True, traces: pd.DataFrame = None) -> float:
    """
    Calculate the Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    
    Returns:
    float: The computed AUC value.
    """
    
    if(validation):
        validate_dataframe(df)

    if traces is None:
        traces = extract_traces_by_session(df)

    traces = traces.sort_values(by='timeStamp')

    traces = compute_space_time_diff(traces)

    # Área bajo la curva real
    area_real = np.trapezoid(traces['y'], traces['x'])

    return area_real

def auc_optimal(df: pd.DataFrame, validation: bool = True, traces: pd.DataFrame = None) -> float:
    """
    Calculate the Optimal Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    
    Returns:
    float: The computed optimal AUC value.
    """
    
    if(validation):
        validate_dataframe(df)
    
    if traces is None:
        traces = extract_traces_by_session(df)


    traces = compute_space_time_diff(traces)

    
    # Área bajo la línea óptima
    x0, y0 = traces['x'].iloc[0], traces['y'].iloc[0]
    x1, y1 = traces['x'].iloc[-1], traces['y'].iloc[-1]
    x_opt = np.linspace(x0, x1, len(df))
    y_opt = np.linspace(y0, y1, len(df))
    area_optimal = np.trapezoid(y_opt, x_opt)

    return area_optimal

def auc_ratio(df: pd.DataFrame, traces:pd.DataFrame = None) -> dict:
    """
    Calculate the AUC ratio for the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
        traces (dict): Optional precomputed traces by sessionId. If None, traces will be extracted from df by sessionId.
    
    Returns:
        auc_per_session (dict): A dictionary with sessionId as keys and a tuple (area_real, area_optimal, auc_ratio) as values.
    """

    validate_dataframe(df)
    
    if traces is None:
        traces = extract_traces_by_session(df)
    
    auc_per_session = {}
    for session_id, session_traces in traces.items():
        area_real = auc(session_traces, False, traces)
        area_optimal = auc_optimal(session_traces, False, traces)
        auc_per_session[session_id] = (area_real, area_optimal, abs(area_real - area_optimal) / (abs(area_optimal) + 1e-6))

    return auc_per_session

def num_pauses(df: pd.DataFrame, threshold: float = 100, traces: pd.DataFrame = None) -> tuple[dict, dict]:
    """
    Calculate the number of pauses in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' column.
        threshold (float): Time threshold in milliseconds to consider a pause, by default 100 ms.
        traces (dict): Optional precomputed traces by sessionId. If None, traces will be extracted from df by sessionId.
    
    Returns:
        tuple: A tuple containing two dictionaries with the number of pauses per session and the mean number of pauses per trace, with the sessionId as keys.
    """
    validate_dataframe(df)

    if traces is None:
        traces = extract_traces_by_session(df)

    num_pauses_per_session = {}
    mean_pause_per_trace = {}
    for session_id, session_traces in traces.items():
        total_pauses_session = 0
        for trace in session_traces:
            df_pauses = _num_pauses_trace(trace, threshold)
            total_pauses_session += df_pauses.shape[0]
        num_pauses_per_session[session_id] = total_pauses_session
        mean_pause_per_trace[session_id] = total_pauses_session / len(session_traces) if len(session_traces) > 0 else 0
    return num_pauses_per_session, mean_pause_per_trace

def _num_pauses_trace(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Helper function to calculate pauses in a single trace.
    """
    df = df.sort_values(by='timeStamp').reset_index(drop=True)
    df['dt'] = df['timeStamp'].diff().fillna(0)
    pauses = df[df['dt'] > threshold]
    return pauses