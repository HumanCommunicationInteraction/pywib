import pandas as pd
from ..constants import EventTypes


def extract_trace(dt: pd.DataFrame) -> list:
    """
    Extracts trace from the DataFrame.
    Each trace is a sequence of consecutive ON_MOUSE_MOVE events
    between two non-move events.
    Returns a list of DataFrames, each corresponding to a trace.
    """
    dt = dt.sort_values(by='timeStamp').reset_index(drop=True)
    is_move = (dt['eventType'] == EventTypes.EVENT_ON_MOUSE_MOVE) | (dt['eventType'] == EventTypes.EVENT_ON_TOUCH_MOVE)
    group_id = (~is_move).cumsum()
    traces = []
    for _, group in dt[is_move].groupby(group_id[is_move]):
        if len(group) > 1:
            traces.append(group)
    return traces