"""
"""

__version__ = "0.1.0"
__author__ = "Guillermo Dylan Carvajal Aza"
__email__ = "carvajalguillermo@uniovi.es"

from .constants import *
from .utils import validate_dataframe, validate_dataframe_keyboard, extract_trace, visualize_trace
from .core.movement import velocity, acceleration, num_pauses, auc_ratio

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
    "num_pauses",
    "auc_ratio"
]