import matplotlib.pyplot as plt

def visualize_trace(df, stroke_indices, stroke_id):
    """"
    Geenrates a plot visualizing the trace of a stroke.

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

