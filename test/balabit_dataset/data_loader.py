import pandas as pd
import numpy as np
import os
from pathlib import Path
from typing import Dict, List, Tuple


# Event type mappings from button and state combinations
EVENT_TYPE_MAPPING = {
    ('NoButton', 'Move'): 0,
    ('Left', 'Pressed'): 3,
    ('Left', 'Released'): 4,
    ('Right', 'Pressed'): 20,
    ('Right', 'Released'): 21,
    ('Scroll', 'Up'): 11,
    ('Scroll', 'Down'): 11,
    ('NoButton', 'Drag'): 3,
}

EVENT_TYPE_MOUSE_CLICK = 2
EVENT_TYPE_SCROLL_WHEEL = 5


def load_session_file(file_path: str) -> pd.DataFrame:
    """
    Load a single session CSV file and return a DataFrame with transformed data.
    
    Args:
        file_path: Path to the session CSV file
        
    Returns:
        DataFrame with columns: x, y, timeStamp, eventType, sessionId
    """
    df = pd.read_csv(file_path)
    
    # Extract session ID from filename (session_XXXXX)
    session_id = Path(file_path).stem.split("_")[1]  # e.g., "session_0335985747" -> "0335985747"
    
    # Create event type from button and state combinations
    df['eventType'] = df.apply(
        lambda row: EVENT_TYPE_MAPPING.get(
            (row['button'], row['state']), 
            -1  # Unknown event type
        ), 
        axis=1
    )
    
    # Keep only relevant columns
    df = df[['x', 'y', 'client timestamp', 'eventType']].copy()
    df.rename(columns={'client timestamp': 'timeStamp'}, inplace=True)
    df['sessionId'] = session_id
    
    # Convert coordinates to numeric
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df['timeStamp'] = pd.to_numeric(df['timeStamp'], errors='coerce')
    
    return df


def generate_intermediate_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate intermediate events:
    1. For each pair of (Left,Pressed) and (Left,Released), generate a mouse click event
    2. For each Scroll event, generate an additional wheel event
    
    Args:
        df: DataFrame with eventType column
        
    Returns:
        DataFrame with intermediate events added
    """
    rows_to_add = []
    
    for session_id in df['sessionId'].unique():
        session_df = df[df['sessionId'] == session_id].copy().reset_index(drop=True)
        
        # Process mouse clicks (Left,Pressed followed by Left,Released)
        i = 0
        while i < len(session_df):
            if session_df.iloc[i]['eventType'] == 3:  # Left Pressed
                # Look for the next Left Released event
                j = i + 1
                while j < len(session_df) and session_df.iloc[j]['eventType'] != 4:
                    j += 1
                
                if j < len(session_df) and session_df.iloc[j]['eventType'] == 4:  # Found Release
                    # Create intermediate click event
                    pressed_row = session_df.iloc[i]
                    released_row = session_df.iloc[j]
                    
                    # Intermediate timestamp (average of both)
                    intermediate_ts = (pressed_row['timeStamp'] + released_row['timeStamp']) / 2
                    
                    # Use coordinates from released event as per spec
                    click_event = {
                        'x': released_row['x'],
                        'y': released_row['y'],
                        'timeStamp': intermediate_ts,
                        'eventType': EVENT_TYPE_MOUSE_CLICK,
                        'sessionId': session_id
                    }
                    rows_to_add.append(click_event)
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1
        
        # Process scroll events
        for idx, row in session_df.iterrows():
            if row['eventType'] == 11:  # Scroll event
                # Generate additional wheel event one nanosecond later
                wheel_event = {
                    'x': row['x'],
                    'y': row['y'],
                    'timeStamp': row['timeStamp'] + 1e-9,  # One nanosecond later
                    'eventType': EVENT_TYPE_SCROLL_WHEEL,
                    'sessionId': session_id
                }
                rows_to_add.append(wheel_event)
    
    # Add new rows to DataFrame
    if rows_to_add:
        new_rows_df = pd.DataFrame(rows_to_add)
        df = pd.concat([df, new_rows_df], ignore_index=True)
    
    return df


def handle_duplicate_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle multiple events with identical sequential timestamps according to rules:
    1. If multiple events have the same timestamp, keep the non-Move event
    2. If all are Move events, keep one Move event
    3. If there are multiple non-Move events, separate them by adding nanoseconds
    
    Args:
        df: DataFrame with eventType and timeStamp columns
        
    Returns:
        DataFrame with duplicate timestamps handled
    """
    df = df.sort_values(by=['sessionId', 'timeStamp']).reset_index(drop=True)
    
    rows_to_keep = []
    i = 0
    
    while i < len(df):
        current_ts = df.iloc[i]['timeStamp']
        current_session = df.iloc[i]['sessionId']
        
        # Find all rows with the same timestamp and session
        j = i + 1
        while j < len(df) and df.iloc[j]['timeStamp'] == current_ts and df.iloc[j]['sessionId'] == current_session:
            j += 1
        
        # Group of rows from index i to j-1 have the same timestamp
        group = df.iloc[i:j].copy().reset_index(drop=True)
        
        if len(group) == 1:
            rows_to_keep.append(group.iloc[0])
            i = j
            continue
        
        # Separate Move events (type 0) from non-Move events
        move_events = group[group['eventType'] == 0]
        non_move_events = group[group['eventType'] != 0]
        
        if len(non_move_events) == 0:
            # All are Move events, keep the first one with last coordinates
            row = group.iloc[-1].copy()
            rows_to_keep.append(row)
        elif len(non_move_events) == 1:
            # One non-Move event, keep it
            rows_to_keep.append(non_move_events.iloc[0])
        else:
            # Multiple non-Move events, separate them by adding nanoseconds
            for idx, non_move_row in non_move_events.iterrows():
                modified_row = non_move_row.copy()
                # Add nanoseconds based on position (to maintain order)
                modified_row['timeStamp'] = current_ts + idx * 1e-9
                rows_to_keep.append(modified_row)
        
        i = j
    
    result_df = pd.DataFrame(rows_to_keep).reset_index(drop=True)
    return result_df


def load_all_sessions(train_folder: str, user_ids: List[int]) -> pd.DataFrame:
    """
    Load all session files from the train folder for specified users.
    
    Args:
        train_folder: Path to the train folder containing user directories
        user_ids: List of user IDs to load (e.g., [9, 12, 15, ...])
        
    Returns:
        Combined DataFrame with all sessions
    """
    all_dfs = []
    
    for user_id in user_ids:
        user_folder = os.path.join(train_folder, f'user{user_id}')
        
        if not os.path.exists(user_folder):
            print(f"Warning: User folder not found: {user_folder}")
            continue
        
        # Get all session files (no extension)
        session_files = sorted([
            os.path.join(user_folder, f)
            for f in os.listdir(user_folder)
            if f.startswith('session_')
        ])
        
        for session_file in session_files:
            try:
                df = load_session_file(session_file)
                all_dfs.append(df)
            except Exception as e:
                print(f"Error loading {session_file}: {e}")
    
    if not all_dfs:
        return pd.DataFrame(columns=['x', 'y', 'timeStamp', 'eventType', 'sessionId'])
    
    # Combine all DataFrames
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Generate intermediate events for clicks and scrolls
    combined_df = generate_intermediate_events(combined_df)
    
    # Handle duplicate timestamps
    combined_df = handle_duplicate_timestamps(combined_df)
    
    # Ensure column order
    combined_df = combined_df[['x', 'y', 'timeStamp', 'eventType', 'sessionId']]
    
    return combined_df
