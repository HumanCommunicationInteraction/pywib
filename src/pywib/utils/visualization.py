import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
from pywib.constants import EventTypes

from pywib.constants import ColumnNames

def visualize_trace(df, stroke_indices, stroke_id):
    """
    Generates a plot visualizing the trace of a stroke.

    Parameters:
        df (pd.DataFrame): DataFrame containing the stroke data with 'x', 'y and 'timeStamp' columns.
        stroke_indices (list): List of indices corresponding to the stroke in the DataFrame. Can be obtained using df.index.
        stroke_id (str): Identifier for the stroke to be displayed in the title.
    Returns:
        None: Displays a plot of the stroke trace.
    """
    stroke_data = df.loc[stroke_indices]
    plt.figure(figsize=(10, 8))
    plt.plot(stroke_data['x'], stroke_data['y'], 'b-o', linewidth=2, markersize=4, label='Trazo real')

    x_start, y_start = stroke_data['x'].iloc[0], stroke_data['y'].iloc[0]
    x_end, y_end = stroke_data['x'].iloc[-1], stroke_data['y'].iloc[-1]
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

def video_from_trace(df, user_id, outfile: str, width=640, height=480, fps=30, colored=False):
    """
    Generates a video visualizing the mouse trace of a user.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the mouse trace data with 'x', 'y', 'eventType', and 'sessionId' columns.
        user_id (str/int): Identifier of the user whose trace is to be visualized.
        outfile (str): Path to save the output video file.
        width (int): Width of the video frame.
        height (int): Height of the video frame.
        fps (int): Frames per second for the video.
        colored (bool): If True, applies a temperature gradient (green to red) to the trajectory line.
    Returns:
        None: Saves the video file to the specified path.
    """
    user_data = df[df[ColumnNames.SESSION_ID] == user_id].sort_values(ColumnNames.TIME_STAMP)
    xs = user_data[ColumnNames.X].values
    ys = user_data[ColumnNames.Y].values
    eventType = user_data[ColumnNames.EVENT_TYPE].values
    n = len(xs)
    # Nombre del vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(outfile, fourcc, fps, (width, height))
    
    # Generar frames
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # fondo blanco
    last_x, last_y = xs[0], ys[0]
    for i in range(1, n):
        # Calculate color based on progress if colored mode is enabled
        if colored:
            # Temperature gradient: green (0, 255, 0) -> yellow -> red (0, 0, 255)
            progress = i / (n - 1)
            green = int(255 * (1 - progress))
            red = int(255 * progress)
            line_color = (0, green, red)  # BGR format
        else:
            line_color = (0, 0, 255)  # Default red
        
        # Dibujar línea de movimiento
        if xs[i] <= 0 or ys[i] <= 0 or xs[i] > width or ys[i] > height:
            # Coordenadas fuera de la pantalla, no dibujar
            pass
        elif xs[i-1] <= 0 or ys[i-1] <= 0 or xs[i-1] > width or ys[i-1] > height:
            # Coordenadas anteriores fuera de la pantalla
            if(last_x > 0 and last_y > 0):
                cv2.line(frame, (last_x, last_y), (xs[i], ys[i]), color=line_color, thickness=2)
        else:
            cv2.line(frame, (xs[i-1], ys[i-1]), (xs[i], ys[i]), color=line_color, thickness=2)
        
        # Actualizar última posición válida a la posición actual si es válida (dentro de la pantalla)
        if xs[i] > 0 and ys[i] > 0 and xs[i] <= width and ys[i] <= height:
            last_x, last_y = xs[i], ys[i]

        # Dibujar clics
        if eventType[i] == EventTypes.EVENT_ON_CLICK or (eventType[i-1] == EventTypes.EVENT_ON_MOUSE_DOWN and eventType[i] == EventTypes.EVENT_ON_MOUSE_UP):
            cv2.circle(frame, (last_x, last_y), radius=5, color=(0, 0, 255), thickness=-1)
        elif eventType[i] == EventTypes.EVENT_KEY_DOWN or eventType[i] == EventTypes.EVENT_KEY_UP:
            # This event has coordinates (0,0) or (-1,-1)
            cv2.rectangle(frame, (last_x-5, last_y-5), (last_x+5, last_y+5), color=(255, 0, 0), thickness=-1)
        elif eventType[i] == EventTypes.EVENT_WINDOW_SCROLL:
            # This event has coordinates (0,0) or (-1,-1)
            pts = np.array([(last_x, last_y-5), (last_x-5, last_y+5), (last_x+5, last_y+5)], np.int32)
            cv2.polylines(frame, [pts], True, (255, 0, 0), 2)
        else:
            # Unknown or unhandled event type
            pass
        
        # Escribir frame en vídeo
        video.write(frame.copy())
    
    video.release()
    print(f"Vídeo generado para el usuario {user_id}: {outfile}")