"""
Core metrics functions from PyWib
"""
from .timing import execution_time, movement_time, num_pauses, pauses_metrics
from .movement import (velocity, acceleration, jerkiness, auc,
                       velocity_metrics, acceleration_metrics, jerkiness_metrics,
                       deviations, path)
from .mouse import click_slip, number_of_clicks
from .keyboard import (typing_speed, typing_speed_metrics, backspace_usage, typing_durations)

__all__ = [
    "execution_time",
    "movement_time",
    "num_pauses",
    "pauses_metrics",
    "velocity",
    "acceleration",
    "jerkiness",
    "path",
    "auc",
    "velocity_metrics",
    "acceleration_metrics",
    "jerkiness_metrics",
    "click_slip",
    "number_of_clicks",
    "deviations"
    "typing_speed",
    "typing_speed_metrics",
    "backspace_usage",
    "typing_durations",
    "typing_speed"
]