"""
"""

__version__ = "0.1.0"
__author__ = "Guillermo Dylan Carvajal Aza"
__email__ = "carvajalguillermo@uniovi.es"

from .constants import *
from .utils import validate_dataframe, validate_dataframe_keyboard, extract_traces_by_session, visualize_trace, compute_space_time_diff
from .core import (velocity, acceleration, jerkiness, path, auc_ratio, 
                   execution_time, movement_time, pauses_metrics, velocity_metrics)
__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__email__",

    # Constants
    "EventTypes",
    "ComponentTypes",
    
    # Utility functions
    "validate_dataframe",
    "validate_dataframe_keyboard",
    "extract_trace",
    "visualize_trace",

    # Movement functions
    "velocity",
    "acceleration",
    "auc_ratio",
    "jerkiness",
    "path",
    "velocity_metrics"

    # Timing
    "pauses_metrics",
    "execution_time",
    "movement_time",

    # Utils
    "compute_space_time_diff",
    "extract_traces_by_session",
]