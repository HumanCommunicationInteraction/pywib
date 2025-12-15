
import pandas as pd
import numpy as np
from pywib.constants import ColumnNames, EventTypes
from pywib.utils.validation import validate_dataframe_keyboard 

def typing_durations_df(df: pd.DataFrame = None) -> list:
    """
    Calculate the durations of individual keystrokes from a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp and 'key' columns.
    Returns:
        list: List of keystroke durations in milliseconds.
    """

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

def typing_durations_traces(traces: dict[str, list[pd.DataFrame]]) -> dict[str, list[pd.DataFrame]]:
    """
    Calculate the durations of individual keystrokes from pre-extracted keystroke traces.

    Parameters:
        traces (dict[str, list[pd.DataFrame]]): Pre-extracted keystroke traces by session.
    Returns:
        dict (dict[str, list[pd.DataFrame]]): A dictionary with session IDs as keys and lists of keystroke durations per trace as values.
    """
    durations_per_session = {}
    for session_id, keystroke_traces in traces.items():
        durations = []
        for trace in keystroke_traces:
            trace_durations = typing_durations_df(trace)
            durations.append(trace_durations)
        durations_per_session[session_id] = durations
    return durations_per_session