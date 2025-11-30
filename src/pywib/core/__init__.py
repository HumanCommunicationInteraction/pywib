"""
Utility functions for PyWib
"""
from .timing import execution_time, movement_time, num_pauses, pauses_metrics
from .movement import (velocity, acceleration, jerkiness, 
                       path, auc_optimal, auc_ratio, auc, auc_ratio_metrics,
                       velocity_metrics, acceleration_metrics, jerkiness_metrics,
                       MAD)
from .mouse import click_slip, number_of_clicks
from .keyboard import (typing_speed, typing_speed_metrics, backspace_usage)

__all__ = [
    "execution_time",
    "movement_time",
    "num_pauses",
    "pauses_metrics",
    "velocity",
    "acceleration",
    "jerkiness",
    "path",
    "auc_optimal",
    "auc_ratio",
    "auc_ratio_metrics",
    "auc",
    "velocity_metrics",
    "acceleration_metrics",
    "jerkiness_metrics",
    "click_slip",
    "number_of_clicks",
    "MAD",
    "typing_speed",
    "typing_speed_metrics",
    "backspace_usage",
]