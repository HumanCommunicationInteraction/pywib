import pandas as pd
import numpy as np
from ..utils.validator import validate_dataframe
from ..utils.utils import compute_space_time_diff

def velocity(df: pd.DataFrame):
    
    # TODO Segmentar en trazas

    validate_dataframe(df)

    df = compute_space_time_diff(df)

    df['velocity'] = df['distance'] / df['dt']
    
    return df

def acceleration(df: pd.DataFrame) -> pd.DataFrame:

    # TODO Segmentar en trazas

    validate_dataframe(df)

    df = compute_space_time_diff(df)
    
    df['acceleration'] = df.groupby(['sessionId', 'sceneId'])['velocity'].diff().fillna(0) / df['dt']

    return df

def path(df: pd.DataFrame) -> pd.DataFrame:

    # TODO Segmentar en trazas

    validate_dataframe(df)
    
    df = compute_space_time_diff(df)

    df['distance'] = np.sqrt(df['dx'] ** 2 + df['dy'] ** 2)

    return df


def auc(df: pd.DataFrame) -> float:
    """
    Calculate the Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    
    Returns:
    float: The computed AUC value.
    """

    # TODO Segmentar en trazas
    
    validate_dataframe(df)

    df = df.sort_values(by='timeStamp')
    
    df = compute_space_time_diff(df)

    # Área bajo la curva real
    area_real = np.trapezoid(df['y'], df['x'])

    return area_real

def auc_optimal(df: pd.DataFrame) -> float:
    """
    Calculate the Optimal Area Under the Curve (AUC) for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    
    Returns:
    float: The computed optimal AUC value.
    """
    
    # TODO Segmentar en trazas

    validate_dataframe(df)

    df = compute_space_time_diff(df)

    
    # Área bajo la línea óptima
    x0, y0 = df['x'].iloc[0], df['y'].iloc[0]
    x1, y1 = df['x'].iloc[-1], df['y'].iloc[-1]
    x_opt = np.linspace(x0, x1, len(df))
    y_opt = np.linspace(y0, y1, len(df))
    area_optimal = np.trapezoid(y_opt, x_opt)

    return area_optimal

def auc_ratio(df: pd.DataFrame) -> float:
    """
    Calculate the AUC ratio for the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'timeStamp' and 'y' columns.
    
    Returns:
    float: The computed AUC ratio value.
    """

    # TODO Segmentar en trazas
    
    validate_dataframe(df)

    area_real = auc(df)
    area_optimal = auc_optimal(df)

    return abs(area_real - area_optimal) / (abs(area_optimal) + 1e-6)
    