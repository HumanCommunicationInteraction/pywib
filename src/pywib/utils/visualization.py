from turtle import width
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
from .segmentation import extract_traces_by_session
from ..constants import ColumnNames, EventTypes

def visualize_trace(df, stroke_indices, stroke_id):
    stroke_data = df.loc[stroke_indices]
    plt.figure(figsize=(10, 8))
    plt.plot(stroke_data[ColumnNames.X], stroke_data[ColumnNames.Y], 'b-o', linewidth=2, markersize=4, label='Trazo real')

    x_start, y_start = stroke_data[ColumnNames.X].iloc[0], stroke_data[ColumnNames.Y].iloc[0]
    x_end, y_end = stroke_data[ColumnNames.X].iloc[-1], stroke_data[ColumnNames.Y].iloc[-1]
    plt.plot([x_start, x_end], [y_start, y_end], 'r--', linewidth=2, label='Línea óptima')

    plt.plot(x_start, y_start, 'go', markersize=8, label='Inicio')
    plt.plot(x_end, y_end, 'ro', markersize=8, label='Fin')

    duration = stroke_data['timeStamp'].iloc[-1] - stroke_data['timeStamp'].iloc[0]
    plt.xlabel('X (píxeles)')
    plt.ylabel('Y (píxeles)')
    plt.title(f'Trazo {stroke_id} - Duración: {duration:.0f}ms - Puntos: {len(stroke_data)}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_yaxis()
    plt.show()

def video_from_traces(df: pd.DataFrame, traces: dict[str, list[pd.DataFrame]] = None, fps: int = 30, video_path: str = './', separate_in_traces: bool = False):
    
    if not separate_in_traces:
        usuarios = df[ColumnNames.SESSION_ID].unique()
        for usuario in usuarios:
            df_usuario = df[df[ColumnNames.SESSION_ID] == usuario].sort_values(ColumnNames.TIME_STAMP)
            _video_from_df(df_usuario, usuario, fps=fps, output_video=f"{video_path}/user_{usuario}.mp4", width=1280, height=720)
        return
    
    if traces is None:
        traces = extract_traces_by_session(df)

    trace_count = 0
    for usuario, session_traces in traces.items():
        # Datos del usuario
        width = 1280
        height = 720

        for trace in session_traces:
            _video_from_df(trace, usuario, fps=fps, output_video=f"{video_path}/trace_{trace_count}_user_{usuario}.mp4", width=width, height=height)
            trace_count += 1

def _video_from_df(df: pd.DataFrame, usuario:str, fps: int = 30, output_video: str = '', width: int = 1280, height: int = 720):
    df = _replace_zero_coord(df)
    xs = df[ColumnNames.X]
    ys = df[ColumnNames.Y]
    eventType = df[ColumnNames.EVENT_TYPE]
    n = len(xs)
    # Nombre del vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Generar frames
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # fondo blanco
    for i in range(1, n):
        # Dibujar línea de movimiento
        cv2.line(frame, (xs[i-1], ys[i-1]), (xs[i], ys[i]), color=(0, 0, 255), thickness=2)
        
        # Dibujar clics
        if eventType[i] == EventTypes.EVENT_ON_CLICK:
            cv2.rectangle(frame, (xs[i]-5, ys[i]-5), (xs[i]+5, ys[i]+5), color=(0, 0, 255), thickness=-1)
        elif eventType[i] == EventTypes.EVENT_KEY_DOWN or eventType[i] == EventTypes.EVENT_KEY_PRESS:
            cv2.circle(frame, (xs[i - 1], ys[i - 1]), radius=5, color=(255, 0, 0), thickness=-1)
        # Escribir frame en vídeo
        video.write(frame.copy())
    
    video.release()
    print(f"Video generated for user {usuario}: {output_video}")

def _replace_zero_coord(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces zero coordinates in the DataFrame with the last known non-zero coordinates.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'x' and 'y' columns.

    Returns:
    pd.DataFrame: DataFrame with zero coordinates replaced.
    """
    df = df.copy()
    last_x, last_y = None, None

    for i in range(len(df)):
        if df.at[i, ColumnNames.X] > 0 and df.at[i, ColumnNames.Y] > 0:
            last_x, last_y = df.at[i, ColumnNames.X], df.at[i, ColumnNames.Y]
        else:
            if last_x is not None and last_y is not None:
                df.at[i, ColumnNames.X], df.at[i, ColumnNames.Y] = last_x, last_y

    return df