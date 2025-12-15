
import pandas as pd
import numpy as np
from pywib.constants import ColumnNames, EventTypes, KeyCodeEvents
from pywib.utils.validation import validate_dataframe_keyboard 

def typing_durations_df(df: pd.DataFrame = None, validate: bool = True) -> list:
    """
    Calculate the durations of individual keystrokes from a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp and 'key' columns.
        validate (bool): Whether to validate the input DataFrame. Default is True.
    Returns:
        list: List of keystroke durations in milliseconds.
    """
    if validate:
        validate_dataframe_keyboard(df)
    durations = []

    key_down_events = df[df[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_DOWN]
    key_up_events = df[df[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_UP]
    for key in key_down_events[ColumnNames.KEY].unique():
        down_times = key_down_events[key_down_events[ColumnNames.KEY] == key][ColumnNames.TIME_STAMP].values
        up_times = key_up_events[key_up_events[ColumnNames.KEY] == key][ColumnNames.TIME_STAMP].values
        paired_times = zip(down_times, up_times)
        for down_time, up_time in paired_times:
            duration = up_time - down_time
            if duration >= 0:
                durations.append(duration)
    return durations

def typing_durations_traces(traces: dict[str, list[pd.DataFrame]], validate: bool = True) -> dict[str, list[pd.DataFrame]]:
    """
    Calculate the durations of individual keystrokes from pre-extracted keystroke traces.

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Pre-extracted keystroke traces by session.
        validate (bool): Whether to validate the input DataFrames. Default is True.
    Returns:
        dict (dict[str, list[pd.DataFrame]]): A dictionary with session IDs as keys and lists of keystroke durations per trace as values.
    """
    durations_per_session = {}
    for session_id, keystroke_traces in traces.items():
        durations = []
        for trace in keystroke_traces:
            trace_durations = typing_durations_df(trace, validate)
            durations.append(trace_durations)
        durations_per_session[session_id] = durations
    return durations_per_session

def typing_speed_df(df: pd.DataFrame = None, validate: bool = True) -> float:
    """
    Calculate the average typing speed in characters per minute (CPM) from a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        validate (bool): Whether to validate the input DataFrame. Default is True.
    Returns:
        float: Average typing speed in characters per minute (CPM).
    """
    
    if validate:
        validate_dataframe_keyboard(df)
    total_chars = 0
    total_time = 0.0  # in seconds
    strokes = df[df[ColumnNames.EVENT_TYPE].isin([EventTypes.EVENT_KEY_UP, EventTypes.EVENT_KEY_DOWN])]
    keys = df[df[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_UP]
    total_chars += len(keys)
    if not strokes.empty:
        time_start = strokes[ColumnNames.TIME_STAMP].iloc[0]
        time_end = strokes[ColumnNames.TIME_STAMP].iloc[-1]
        total_time = (time_end - time_start) / 1000.0  # convert ms to s
        if total_time > 0:
            cpm = (total_chars / total_time) * 60.0
            return cpm
    return 0.0

def typing_speed_traces(traces: dict[str, list[pd.DataFrame]], validate: bool = True) -> dict[str, list[float]]:
    """
    Calculate the average typing speed in characters per minute (CPM) from pre-extracted keystroke traces.

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Pre-extracted keystroke traces by session.
        validate (bool): Whether to validate the input DataFrames. Default is True.
    Returns:
        dict (dict[str, list[float]]): A dictionary with session IDs as keys and lists of typing speeds (CPM) per trace as values.
    """
    speed_by_session = {}
    for session_id, keystroke_traces in traces.items():
        speed_by_trace = []
        for trace in keystroke_traces:
            cpm = typing_speed_df(trace, validate)
            speed_by_trace.append(cpm)
        speed_by_session[session_id] = speed_by_trace
    return speed_by_session

def backspace_usage_df(df: pd.DataFrame = None, validate: bool = True) -> float:
    """
    Calculate the backspace usage rate as a percentage of total keystrokes from a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        validate (bool): Whether to validate the input DataFrame. Default is True.
    Returns:
        float: Backspace usage rate as a percentage of total keystrokes.
    """
    if validate:
        validate_dataframe_keyboard(df)
    mask = (df[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_DOWN) & ( (df[ColumnNames.KEY_CODE_EVENT] == KeyCodeEvents.KEY_CODE_BACKSPACE) | (df[ColumnNames.KEY_CODE_EVENT] == KeyCodeEvents.KEY_CODE_DELETE))

    return int(mask.sum())

def backspace_usage_traces(traces: dict[str, list[pd.DataFrame]], validate: bool = True) -> dict[str, list[float]]:
    """
    Calculate the backspace usage rate as a percentage of total keystrokes from pre-extracted keystroke traces.

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Pre-extracted keystroke traces by session.
        validate (bool): Whether to validate the input DataFrames. Default is True.
    Returns:
        dict (dict[str, list[float]]): A dictionary with session IDs as keys and lists of backspace usage rates per trace as values.
    """
    usage_by_session = {}
    for session_id, keystroke_traces in traces.items():
        backspace_count = 0
        for trace in keystroke_traces:
            usage = backspace_usage_df(trace, validate)
            backspace_count += usage
        usage_by_session[session_id] = backspace_count
    return usage_by_session