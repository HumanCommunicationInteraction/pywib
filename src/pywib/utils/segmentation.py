import pandas as pd
from ..constants import EventTypes, ColumnNames
from ..utils.validation import validate_dataframe, validate_dataframe_keyboard

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
    Parameters:
        dt (pd.DataFrame): DataFrame containing 'sessionId', 'sceneId', 'eventType', and 'timeStamp' columns.
    Returns:
        dict: a dictionary with keys as (sessionId) and values as lists of DataFrames.
    """
    validate_dataframe(dt)
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    traces_by_session = {}
    for session_id, group in dt.groupby(ColumnNames.SESSION_ID):
        is_move = group[ColumnNames.EVENT_TYPE].isin([EventTypes.EVENT_ON_MOUSE_MOVE, EventTypes.EVENT_ON_TOUCH_MOVE])
        group_id = (~is_move).cumsum()
        traces = []
        for _, sub_group in group[is_move].groupby(group_id[is_move]):
            if len(sub_group) > 1:
                traces.append(sub_group)
        traces_by_session[session_id] = traces
    return traces_by_session

def extract_keystroke_traces_by_session(dt: pd.DataFrame) -> dict[str, list[pd.DataFrame]]:
    """
    Extracts keystroke traces from the DataFrame, grouped by (sessionId, sceneId).
    Each keystroke trace is considered as a sequence of consecutive key events
    between two non-keyboard events.
    Parameters:
        dt (pd.DataFrame): DataFrame containing 'sessionId', 'sceneId', 'eventType', and 'timeStamp' columns.
    Returns:
        dict: a dictionary with keys as (sessionId) and values as lists of DataFrames.
    """
    validate_dataframe_keyboard(dt)
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    keystroke_traces_by_session = {}
    for session_id, group in dt.groupby(ColumnNames.SESSION_ID):
        is_keydown = group[ColumnNames.EVENT_TYPE].isin([EventTypes.EVENT_KEY_UP, EventTypes.EVENT_KEY_DOWN, EventTypes.EVENT_KEY_PRESS])
        group_id = (~is_keydown).cumsum()
        keystroke_traces = []
        for _, sub_group in group[is_keydown].groupby(group_id[is_keydown]):
            if len(sub_group) > 0:
                keystroke_traces.append(sub_group)
        keystroke_traces_by_session[session_id] = keystroke_traces
    return keystroke_traces_by_session
    
def extract_mouse_click_traces_by_ession(dt: pd.DataFrame) -> dict:
    """
    Extracts those traces with event movements that end with ON_MOUSE_CLICK or ON_TOUCH_TAP events,
    grouped by sessionId.
    """
    validate_dataframe(dt)
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    click_traces_by_session = {}
    for session_id, group in dt.groupby(ColumnNames.SESSION_ID):
        is_move = (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_MOVE) | (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_TOUCH_MOVE)
        group_id = (~is_move).cumsum()
        click_traces = []
        for _, sub_group in group[is_move].groupby(group_id[is_move]):
            if len(sub_group) > 1:
                last_index = sub_group.index[-1]
                # get the integer position of last_index within `group`'s index to avoid assuming contiguous indices
                try:
                    pos = group.index.get_loc(last_index)
                except KeyError:
                    # if for some reason the index is not found, skip this sub_group
                    continue
                if pos + 1 < len(group):
                    next_event = group.iloc[pos + 1][ColumnNames.EVENT_TYPE]
                    if next_event in [EventTypes.EVENT_ON_CLICK, EventTypes.EVENT_ON_MOUSE_DOWN, EventTypes.EVENT_ON_MOUSE_UP]:
                        click_traces.append(sub_group)
        click_traces_by_session[session_id] = click_traces
    return click_traces_by_session

def extract_mouse_click_traces_by_session_with_intial_pause(dt: pd.DataFrame, pause_threshold: float = 200) -> dict:
    dt = dt.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
    click_traces_by_session = {}
    for session_id, group in dt.groupby(ColumnNames.SESSION_ID):
        is_move = (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_MOUSE_MOVE) | (group[ColumnNames.EVENT_TYPE] == EventTypes.EVENT_ON_TOUCH_MOVE)
        group_id = (~is_move).cumsum()
        click_traces = []
        for _, sub_group in group[is_move].groupby(group_id[is_move]):
            if len(sub_group) > 1:
                last_index = sub_group.index[-1]
                # get the integer position of last_index within `group`'s index to avoid assuming contiguous indices
                try:
                    pos = group.index.get_loc(last_index)
                except KeyError:
                    # if for some reason the index is not found, skip this sub_group
                    continue
                if pos + 1 < len(group):
                    next_event = group.iloc[pos + 1][ColumnNames.EVENT_TYPE]
                    if next_event in [EventTypes.EVENT_ON_CLICK, EventTypes.EVENT_ON_MOUSE_DOWN, EventTypes.EVENT_ON_MOUSE_UP]:
                        sub_group = sub_group.sort_values(by=ColumnNames.TIME_STAMP).reset_index(drop=True)
                        sub_group[ColumnNames.DT] = sub_group[ColumnNames.TIME_STAMP].diff().fillna(0)
                        pauses = sub_group[sub_group[ColumnNames.DT] > pause_threshold]
                        # Now check if there is a pause at the beginning and no pauses in between
                        if not pauses.empty and pauses.index[0] == 1 and pauses.shape[0] == 1:
                            click_traces.append(sub_group)

        click_traces_by_session[session_id] = click_traces
    return click_traces_by_session