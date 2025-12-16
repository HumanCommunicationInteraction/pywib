"""
Analysis module for HCI Web Interaction Analyzer

This module provides methods to analyze interaction data from DataFrames.
"""

import pandas as pd
import numpy as np
from pywib.utils.segmentation import extract_keystroke_traces_by_session
from pywib.utils.validation import validate_dataframe_keyboard
from pywib.constants import EventTypes, ColumnNames
from pywib.utils.keyboard import (backspace_usage_df, backspace_usage_traces, typing_durations_df, typing_durations_traces, typing_speed_df, typing_speed_traces)

def typing_durations(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces: bool = True) -> list:
    """
    Calculate the durations of individual keystrokes.

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces (dict[str, list[pd.DataFrame]]): optional Pre-extracted keystroke traces by session.
        per_traces (bool): optional Whether to calculate durations per trace. Default is True.
    Returns:
        list: List of keystroke durations in milliseconds.
    """
    if traces is None and per_traces:
        traces = extract_keystroke_traces_by_session(df)
        return typing_durations_traces(traces, False)

    if not per_traces:
        return typing_durations_df(df)

    return typing_durations_traces(traces)

def typing_speed(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None, per_traces : bool = True) -> dict[list[float]] | float:
    """
    Calculate the average typing speed in characters per minute (CPM).

    Parameters:
        df (pd.DataFrame): DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces (dict[str, list[pd.DataFrame]]): optional Pre-extracted keystroke traces by session.
        per_traces (bool): optional Whether to calculate speed per trace. Default is True. if False, mind that the df must only contain typing data in order to obtain the correct CPM calculation.

    Returns:
        dict (dict[list[float]] | float) : A dictionary with session IDs as keys and lists of typing speeds (CPM) per trace as values, or a float representing the typing speed if per_traces is False.
    """

    if per_traces and traces is None:
        traces = extract_keystroke_traces_by_session(df)
        return typing_speed_traces(traces, False)

    elif not per_traces:
        return typing_speed_df(df)

    return typing_speed_traces(traces)

def typing_speed_metrics(df: pd.DataFrame = None, traces: dict[str, list[pd.DataFrame]] = None) -> dict:
    """
    Calculate typing speed metrics including average CPM, total characters typed, and total time spent typing.

    Parameters:
        df : pd.DataFrame DataFrame containing interaction data with 'event_type', 'timestamp', and 'key' columns.
        traces : dict[str, list[pd.DataFrame]], optional Pre-extracted keystroke traces by session.
        per_trace : bool, optional Whether to calculate metrics per trace. Default is True.
    Returns:
        dict: A dictionary with session IDs as keys and their corresponding typing speed metrics as values. This metrics include average typing speed (CPM), total characters typed, and total time spent typing (in seconds).
    """
    if traces is None:
        traces = extract_keystroke_traces_by_session(df)
    
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
                "avg_keydown_to_keyup_duration": -1  # TODO Placeholder for future implementation
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
        return backspace_usage_traces(traces, False)
    if not per_trace:
        validate_dataframe_keyboard(df)
        return backspace_usage_df(df)
    
    return backspace_usage_traces(traces)