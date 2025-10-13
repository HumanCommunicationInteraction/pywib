"""
Utility functions for PyWib
"""
from .timing import execution_time, movement_time, num_pauses, pauses_metrics
from .movement import (velocity, acceleration, jerkiness, 
                       path, auc_optimal, auc_ratio, auc, 
                       velocity_metrics, acceleration_metrics, jerkiness_metrics)
from .mouse import click_slip, number_of_clicks

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
    "auc",
    "velocity_metrics",
    "acceleration_metrics",
    "jerkiness_metrics"
]