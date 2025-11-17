import pandas as pd
from pywib.utils import validate_dataframe, extract_mouse_click_traces_by_session_with_intial_pause
from pywib.core import auc_ratio

def obtain_straight_patterns(df: pd.DataFrame = None, traces : list[str, list[pd.DataFrame]] = None, per_traces= False, threshold = 100) -> list[pd.DataFrame]:
    """
        First described in 'Investigating the Differences in Web Browsing Behaviour of Chinese and European Users Using Mouse Tracking' (Lee & Chen, 2007),
        the Straight Pattern can be described as a direct or straight movement in direction to a target, characterized by a pause before a direct
        movement towards a target without significant pauses in between the initial movement and the target acquisition.
        
        TODO : initial pause

        Parameters:
            df (pd.DataFrame): DataFrame containing 'sessionId', 'sceneId', 'eventType', 'timeStamp', 'x', and 'y' columns.
            traces (list): List of traces to analyze. Each trace is a pd.DataFrame.
            per_traces (bool): If True, process per traces. Default is False.
            threshold (float): Threshold (in px) for the AUC perpendicular distance to consider a movement as a straight pattern. Default is 100.
        Returns:
            list[pd.DataFrame]: A list of DataFrames, each corresponding to a straight pattern trace.
    """
    if(traces is None and per_traces):
        validate_dataframe(df)
        # This variable will always contain point and click traces
        traces = extract_mouse_click_traces_by_session_with_intial_pause(df)

    if(not per_traces):
        raise NotImplementedError("The 'per_traces' functionality is not yet implemented.")
    
    auc_values = auc_ratio(None, traces= traces, per_traces= True)

    straight_patterns_per_session = {}
    for session_id, trace in auc_values.items():
        straight_patterns = []
        for i, auc in enumerate(trace):
            # TODO usar auc_ratio con un porcentaje del threshold?
            if(auc['auc_perp'] <= threshold):
                straight_patterns.append(traces[session_id][i])
        straight_patterns_per_session[session_id] = straight_patterns
    return straight_patterns_per_session