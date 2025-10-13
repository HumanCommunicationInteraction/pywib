import pandas as pd
import numpy as np
from ..utils.validation import validate_dataframe
from ..utils.utils import compute_space_time_diff
from ..utils.segmentation import extract_traces_by_session
from ..constants import ColumnNames, EventTypes

def number_of_clicks(df: pd.DataFrame) -> dict:
    """
    Calculate the number of clicks per session.
    Parameters:
        df (pd.DataFrame): DataFrame containing mouse event data.
    Returns:
        dict: A dictionary with session IDs as keys and number of clicks as values.
    """
    validate_dataframe(df)

    clicks_per_session = {}
    df = df.groupby(ColumnNames.SESSION_ID)
    for session_id, group in df:
        clicks_per_session[session_id] = group[group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_CLICK].shape[0]
    return clicks_per_session

def click_slip(df: pd.DataFrame, threshold: float = 5.0) -> dict:
    """
    Calculate the number of click slips per session.
    A click slip is defined as a click event that occurs within a certain distance
    from the previous mouse position (indicating an unintended click).

    Parameters:
        df (pd.DataFrame): DataFrame containing mouse event data.
        threshold (float): Distance threshold to consider a click as a slip.

    Returns:
        dict: A dictionary with session IDs as keys and the metrics (click slips, max, min, average) as values.
    """
    validate_dataframe(df)

    click_slips_per_session = {}
    df = df.groupby(ColumnNames.SESSION_ID)
    metrics_per_session = {}
    for session_id, group in df:
        group = group.sort_values(by=ColumnNames.TIME_STAMP)
        slips = 0
        # We define a click slip as: the total path distance of all
        # EVENT_ON_MOUSE_MOVE events that occur between an
        # EVENT_ON_MOUSE_DOWN and the subsequent EVENT_ON_MOUSE_UP.
        # If that total move-distance is less than `threshold` we count
        # it as a slip.
        in_down = False
        last_move_x = None
        last_move_y = None
        accumulated_move_distance = 0.0
        distances = []
        for _, row in group.iterrows():
            # Mouse down: start a new segment
            if row[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_DOWN:
                in_down = True
                # reset accumulators
                last_move_x = row[ColumnNames.X]
                last_move_y = row[ColumnNames.Y]
                accumulated_move_distance = 0.0

            # While between down and up, accumulate move distances
            if in_down and row[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_MOVE:
                x = row[ColumnNames.X]
                y = row[ColumnNames.Y]
                if last_move_x is not None and last_move_y is not None:
                    d = np.hypot(x - last_move_x, y - last_move_y)
                    accumulated_move_distance += d
                # set last seen move position (even if it was the first move)
                last_move_x, last_move_y = x, y

            # Mouse up: finalize the segment and decide if it's a slip
            if row[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_UP and in_down:
                x = row[ColumnNames.X]
                y = row[ColumnNames.Y]
                if last_move_x is not None and last_move_y is not None:
                    d = np.hypot(x - last_move_x, y - last_move_y)
                    accumulated_move_distance += d
                if accumulated_move_distance >= threshold:
                    slips += 1
                    distances.append(accumulated_move_distance)
                in_down = False
                last_move_x = None
                last_move_y = None
                accumulated_move_distance = 0.0
        click_slips_per_session[session_id] = {
            "slips": slips,
            "distances": distances,
        }
        metrics = {
            "click_slips": slips,
            "longest_click_slip": max(distances) if distances else 0,
            "shortest_click_slip": min(distances) if distances else 0,
            "average_click_slip": slips / len(distances) if distances else 0,
            "average_click_slip_distance": np.mean(distances) if distances else 0,
        }
        metrics_per_session[session_id] = metrics
    return metrics_per_session
