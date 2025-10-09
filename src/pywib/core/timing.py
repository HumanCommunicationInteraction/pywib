import pandas as pd
from ..utils.validation import validate_dataframe
from ..utils.segmentation import extract_traces_by_session
from ..utils.utils import compute_space_time_diff
from ..constants import ColumnNames

def execution_time(df: pd.DataFrame) -> dict:
    """
    Calculate the total execution time of a session in milliseconds, without taking pauses into account.
    This is the same as the total time from the first to the last event registered for the session.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' column.
    Returns:
        dict: Total execution time in milliseconds for each session.

    """
    validate_dataframe(df)

    total_time_per_session = {}
    for session_id, session_df in df.groupby(ColumnNames.SESSION_ID):
        session_df = session_df.sort_values(by=ColumnNames.TIME_STAMP)
        total_time = session_df[ColumnNames.TIME_STAMP].iloc[-1] - session_df[ColumnNames.TIME_STAMP].iloc[0]
        total_time_per_session[session_id] = total_time
    return total_time_per_session

def movement_time(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate the total movement time from traces in milliseconds, taking pauses into account.
    This is the same as the interval of time the user is interacting with the interface.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' column.
        traces (dict): Dictionary with sessionId as keys and list of DataFrames as values.
    Returns:
        dict: A dictionary with sessionId as keys and total movement time in milliseconds as values.
    """
    if traces is None:
        validate_dataframe(df)
        traces = extract_traces_by_session(df)

    movement_time_per_session = {}
    for session_id, session_traces in traces.items():
        total_movement_time = 0.0
        for trace in session_traces:
            trace = compute_space_time_diff(trace)  
            total_movement_time += trace[ColumnNames.DT].sum()
        movement_time_per_session[session_id] = total_movement_time

    return movement_time_per_session

def num_pauses(df: pd.DataFrame, threshold: float = 100, computeTraces: bool = True) -> tuple[dict, dict]:
    """
    Calculate the number of pauses in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' column.
        threshold (float): Time threshold in milliseconds to consider a pause, by default 100 ms.
        computeTraces (bool): Whether to compute traces by sessionId, by default True. If False, df is assumed to be already segmented by sessionId.
    
    Returns:
        tuple (tuple[dict, dict]): A tuple containing two dictionaries with the number of pauses per session and the mean number of pauses per trace, with the sessionId as keys.
    """

    if computeTraces:
        validate_dataframe(df)
        df = extract_traces_by_session(df)

    num_pauses_per_session = {}
    mean_pause_per_trace = {}
    for session_id, session_traces in df.items():
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
    df = df.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    df[ColumnNames.DT] = df[ColumnNames.TIME_STAMP].diff().fillna(0)
    pauses = df[df[ColumnNames.DT] > threshold]
    return pauses


def pauses_metrics(df: pd.DataFrame, threshold: float = 100, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate pause metrics for the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'timeStamp' column.
        threshold (float): Time threshold in milliseconds to consider a pause, by default 100 ms.
        traces (dict): Dictionary with sessionId as keys and list of DataFrames as values.

    Returns:
        dict: A dictionary with sessionId as keys and a dictionary of pause metrics as values.
    """

    if traces is None:
        validate_dataframe(df)  
        traces = extract_traces_by_session(df)
    
    pause_metrics_per_session = {}
    number_pauses_session, number_pauses_trace = num_pauses(traces, threshold, computeTraces=False)
    for session_id, session_traces in traces.items():
        total_pauses = 0
        total_pause_duration = 0.0
        pause_durations = []

        for trace in session_traces:
            trace = compute_space_time_diff(trace)  
            pauses = trace[trace[ColumnNames.DT] > threshold]
            total_pauses += pauses.shape[0]
            total_pause_duration += pauses[ColumnNames.DT].sum()
            pause_durations.extend(pauses[ColumnNames.DT].tolist())

        # Compute pause metrics for the session
        if total_pauses > 0:
            mean_pause_duration = total_pause_duration / total_pauses
        else:
            mean_pause_duration = 0

        pause_metrics_per_session[session_id] = {
            "total_pauses": total_pauses,
            "mean_pause_duration": mean_pause_duration,
            "pause_durations": pause_durations,
            "mean_pauses_per_trace": number_pauses_trace.get(session_id, 0),
            "max_pause": max(pause_durations) if pause_durations else 0,
            "min_pause": min(pause_durations) if pause_durations else 0,
        }

    return pause_metrics_per_session