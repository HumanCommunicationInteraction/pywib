"""
Analysis module for HCI Web Interaction Analyzer

This module provides methods to analyze interaction data from DataFrames.
"""

import pandas as pd
import numpy as np
from pywib.utils.segmentation import extract_keystroke_traces_by_session
from pywib.utils.validation import validate_dataframe_keyboard
from pywib.constants import EventTypes, ColumnNames

def typing_durations(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_trace: bool = True) -> list:
    """
    Calculate the durations of individual keystrokes.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces (dict[str, list[pd.DataFrame]]): optional Pre-extracted keystroke traces by session.
        per_trace (bool): optional Whether to calculate durations per trace. Default is True.
    Returns:
        list: List of keystroke durations in milliseconds.
    """
    if traces is None and per_trace:
        traces = extract_keystroke_traces_by_session(df)

    if not per_trace:
        raise NotImplementedError("Calculation without traces is not implemented yet.")

    durations_per_session = {}
    for session_id, keystroke_traces in traces.items():
        durations = []
        for trace in keystroke_traces:
            key_down_events = trace[trace[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_DOWN]
            key_up_events = trace[trace[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_UP]
            for key in key_down_events[ColumnNames.KEY].unique():
                down_times = key_down_events[key_down_events[ColumnNames.KEY] == key][ColumnNames.TIME_STAMP].values
                up_times = key_up_events[key_up_events[ColumnNames.KEY] == key][ColumnNames.TIME_STAMP].values
                paired_times = zip(down_times, up_times)
                for down_time, up_time in paired_times:
                    duration = up_time - down_time
                    if duration >= 0:
                        durations.append(duration)
        durations_per_session[session_id] = durations
    return durations_per_session

def typing_speed(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces : bool = True) -> dict[list[float]]:
    """
    Calculate the average typing speed in characters per minute (CPM).

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces (dict[str, list[pd.DataFrame]]): optional Pre-extracted keystroke traces by session.
        per_traces (bool): optional Whether to calculate speed per trace. Default is True.

    Returns:
        dict (dict[list[float]]) : A dictionary with session IDs as keys and lists of typing speeds (CPM) per trace as values.
    """

    if per_traces and traces is None:
        traces = extract_keystroke_traces_by_session(df)

    elif not per_traces:
        raise NotImplementedError("Calculation without traces is not implemented yet.")

    speed_by_session = {}
    for session_id, keystroke_traces in traces.items():
        speed_by_trace = []
        for trace in keystroke_traces:
            total_chars = 0
            total_time = 0.0  # in seconds
            strokes = trace[trace[ColumnNames.EVENT_TYPE].isin([EventTypes.EVENT_KEY_UP, EventTypes.EVENT_KEY_DOWN])]
            keys = trace[trace[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_UP]
            total_chars += len(keys)
            if not strokes.empty:
                time_start = strokes[ColumnNames.TIME_STAMP].iloc[0]
                time_end = strokes[ColumnNames.TIME_STAMP].iloc[-1]
                total_time = (time_end - time_start) / 1000.0  # convert ms to s
                if total_time > 0:
                    cpm = (total_chars / total_time) * 60.0
                    speed_by_trace.append(cpm)
        speed_by_session[session_id] = speed_by_trace
    return speed_by_session

def typing_speed_metrics(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_trace: bool = True) -> dict:
    """
    Calculate typing speed metrics including average CPM, total characters typed, and total time spent typing.

    Parameters:
        df : pd.DataFrame DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces : dict[str, list[pd.DataFrame]], optional Pre-extracted keystroke traces by session.
        per_trace : bool, optional Whether to calculate metrics per trace. Default is True.
    Returns:
        dict: A dictionary with session IDs as keys and their corresponding typing speed metrics as values. This metrics include average typing speed (CPM), total characters typed, and total time spent typing (in seconds).
    """
    if traces is None and per_trace:
        traces = extract_keystroke_traces_by_session(df)
    
    if not per_trace:
        raise NotImplementedError("Calculation without traces is not implemented yet.")

    session_speeds = typing_speed(None, traces=traces, per_traces=True)

    metrics_by_session = {}
    for session_id, speeds in session_speeds.items():
        if speeds:
            avg_speed = np.mean(speeds)
            total_chars = sum(session_traces[session_traces[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_UP].count() for session_traces in traces[session_id])
            total_time = sum((session_traces[ColumnNames.TIME_STAMP].diff().fillna(0).sum() / 1000.0) for session_traces in traces[session_id])
            metrics_by_session[session_id] = {
                "average_typing_speed": avg_speed,
                "total_characters": total_chars,
                "total_time_seconds": total_time,
                "avg_keydown_to_keyup_duration": -1  # Placeholder for future implementation
            }
    return metrics_by_session


def backspace_usage(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_trace: bool = True) -> dict:
    """
    Calculate the backspace usage rate (backspaces per 100 characters typed) for each session.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces (dict[str, list[pd.DataFrame]]): optional Pre-extracted keystroke traces by session.
        per_trace (bool): optional Whether to calculate usage per trace. Default is True.
    Returns:
        dict: A dictionary with session IDs as keys and their corresponding backspace counts as values.
    """
    if traces is None and per_trace:
        validate_dataframe_keyboard(df)
        traces = extract_keystroke_traces_by_session(df)
    if not per_trace:
        validate_dataframe_keyboard(df)
        raise NotImplementedError("Calculation without traces is not implemented yet.")
    
    times_per_session = {}
    for session_id, keystroke_traces in traces.items():
        backspace_count = 0
        for trace in keystroke_traces:
            backspace_count = 0
            for trace in keystroke_traces:
                mask = (trace[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_KEY_DOWN) & ( (trace[ColumnNames.KEY_CODE_EVENT] == 8) | (trace[ColumnNames.KEY_CODE_EVENT] == 46))
            backspace_count += int(mask.sum())
        times_per_session[session_id] = backspace_count
    return times_per_session