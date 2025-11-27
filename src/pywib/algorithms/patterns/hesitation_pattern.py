import pandas as pd
from pywib.constants import ColumnNames
from pywib.utils import validate_dataframe, extract_mouse_click_traces_by_ession
from pywib.core import velocity, num_pauses

def obtain_unkown_hesitation_patterns(df: pd.DataFrame = None, traces : list[str, list[pd.DataFrame]] = None, per_traces= False, threshold = 100) -> list[pd.DataFrame]:
    """
    Pattern described as:
        "Movements between “two or more answers while trying to decide which one to choose (Ferreira et al., 2010)"
        or
        "The average time from the beginning of a mouse hover to the moment of the mouse click"

    This method aims to identify possible hesitation patterns in mouse movement data without the given positions of the doubted options.
    The results of this function must be further analyzed to confirm if they correspond to hesitation patterns, possibly employing CNN or other ML techniques.
    """
    if(traces is None and per_traces):
        validate_dataframe(df)
        # This variable will always contain point and click traces
        traces = extract_mouse_click_traces_by_ession(df)

    if(not per_traces):
        raise NotImplementedError("The 'per_traces' functionality is not yet implemented.")
    
    # We identify hesitation patterns based on movement characteristics, such as frequent direction changes and pauses.

    vel_traces = velocity(None, traces= traces, per_traces= True)

    hesitation_patterns_per_session = {}
    for session_id, trace_list in vel_traces.items():
        hesitation_patterns = []
        for trace in trace_list:
            # Identify hesitation based on velocity patterns
            # For example, frequent stops and starts or low average velocity
            low_velocity_threshold = 0.1  # Define a threshold for low velocity
            low_velocity_periods = trace[trace[ColumnNames.VELOCITY] < low_velocity_threshold]
            pauses = num_pauses(trace, computeTraces = False)
            # TODO direction changes (X and/or Y flips)
            if len(low_velocity_periods) > 1:  # Arbitrary number of low velocity points to consider as hesitation
                if pauses[session_id]['num_pauses'] >= 1:  # At least 1 pause
                    hesitation_patterns.append(trace)
        hesitation_patterns_per_session[session_id] = hesitation_patterns
    return hesitation_patterns_per_session

