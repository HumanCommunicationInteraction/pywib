import pandas as pd
from ..constants import EventTypes, ColumnNames
from ..utils.validation import validate_dataframe

def extract_trace(dt: pd.DataFrame) -> list:
    """
    Extracts trace from the DataFrame.
    Each trace is considered as a sequence of consecutive ON_MOUSE_MOVE events
    between two non-move events.
    Returns a list of DataFrames, each corresponding to a trace.
    """
    validate_dataframe(dt)
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    is_move = (dt[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_MOVE) | (dt[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_TOUCH_MOVE)
    group_id = (~is_move).cumsum()
    traces = []
    for _, group in dt[is_move].groupby(group_id[is_move]):
        if len(group) > 1:
            traces.append(group)
    return traces

def extract_traces_by_session(dt: pd.DataFrame) -> dict:
    """
    Extracts traces from the DataFrame, grouped by (sessionId, sceneId).
    Each trace is considered as a sequence of consecutive ON_MOUSE_MOVE events
    between two non-move events.

    Returns:
        dict: a dictionary with keys as (sessionId) and values as lists of DataFrames.
    """
    validate_dataframe(dt)
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    traces_by_session = {}
    for session_id, group in dt.groupby(ColumnNames.SESSION_ID):
        is_move = (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_MOVE) | (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_TOUCH_MOVE)
        group_id = (~is_move).cumsum()
        traces = []
        for _, sub_group in group[is_move].groupby(group_id[is_move]):
            if len(sub_group) > 1:
                traces.append(sub_group)
        traces_by_session[session_id] = traces
    return traces_by_session
